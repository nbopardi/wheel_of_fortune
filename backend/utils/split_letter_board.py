import cv2  # type: ignore
import numpy as np  # type: ignore
import argparse
from pathlib import Path
from typing import List, Optional
import re


def find_tile_contours(image: np.ndarray, expected_tiles: int = 33):
    """Detect the 33 tile rectangles in the board image.

    The function now tries BOTH normal and inverted Otsu thresholding and falls back to a
    coarse uniform-grid split if it still cannot find exactly 33 suitable contours. This
    greatly improves robustness against lighting and colour variations between boards."""

    def _threshold_and_find(invert: bool):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        flag = cv2.THRESH_BINARY_INV if invert else cv2.THRESH_BINARY
        _, thresh = cv2.threshold(blur, 0, 255, flag + cv2.THRESH_OTSU)

        # Morphological closing merges inner blemishes, opening removes small noise
        kernel = np.ones((5, 5), np.uint8)
        proc = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
        proc = cv2.morphologyEx(proc, cv2.MORPH_OPEN, kernel, iterations=1)

        contours, _ = cv2.findContours(proc, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    contours = []
    for invert in (False, True):  # try white-on-black then black-on-white
        contours = _threshold_and_find(invert)
        boxes = []
        img_area = image.shape[0] * image.shape[1]
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            area = w * h
            aspect = w / h if h > 0 else 0
            if area < img_area * 0.0005:  # relax area threshold slightly
                continue
            if 0.5 < aspect < 1.5:  # tolerate wider/aspect variability
                boxes.append((x, y, w, h))

        if len(boxes) >= expected_tiles:  # good enough, stop trying further
            break

    # Keep the largest N boxes, then order them
    boxes.sort(key=lambda b: b[2] * b[3], reverse=True)
    boxes = boxes[:expected_tiles]

    if not boxes:
        return []

    # ----- Order boxes into rows/columns -----
    boxes.sort(key=lambda b: b[1])  # primary sort by y (top to bottom)
    rows = []
    current_row = []
    median_h = np.median([h for *_ , h in boxes])
    row_threshold = median_h * 0.6  # y-distance that still counts as the same row
    for b in boxes:
        if not current_row:
            current_row.append(b)
            continue
        if abs(b[1] - current_row[0][1]) < row_threshold:
            current_row.append(b)
        else:
            rows.append(current_row)
            current_row = [b]
    if current_row:
        rows.append(current_row)

    ordered = []
    for r in rows:
        r.sort(key=lambda b: b[0])  # left-to-right
        ordered.extend(r)

    # If we still didn't get exactly the right number, fall back to a calculated uniform grid
    if len(ordered) != expected_tiles:
        h, w = image.shape[:2]
        # assume the board roughly fills the centre third vertically; we slice equally
        top_margin = int(h * 0.2)
        bottom_margin = int(h * 0.2)
        left_margin = int(w * 0.05)
        right_margin = int(w * 0.05)
        grid_w = w - left_margin - right_margin
        grid_h = h - top_margin - bottom_margin
        cell_w = grid_w // 11
        cell_h = grid_h // 3
        ordered = []
        for row_idx in range(3):
            for col_idx in range(11):
                x = left_margin + col_idx * cell_w
                y = top_margin + row_idx * cell_h
                ordered.append((x, y, cell_w, cell_h))

    return ordered


def _pad_to_canvas(img: np.ndarray, canvas_size: tuple[int, int]) -> np.ndarray:
    """Return *img* centred on a black canvas of *canvas_size* (width, height)."""
    target_w, target_h = canvas_size
    h, w = img.shape[:2]
    if target_w < w or target_h < h:
        # If canvas smaller than image, just return original (no padding)
        return img

    diff_w = target_w - w
    diff_h = target_h - h
    left = diff_w // 2
    right = diff_w - left
    top = diff_h // 2
    bottom = diff_h - top
    return cv2.copyMakeBorder(
        img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0, 0, 0)
    )


def _expand_box(x: int, y: int, w: int, h: int, margin: float, img_w: int, img_h: int):
    """Expand box by *margin* fraction of its size on all sides, clamped to image bounds."""
    if margin <= 0:
        return x, y, w, h
    expand_w = int(w * margin)
    expand_h = int(h * margin)
    new_x = max(0, x - expand_w)
    new_y = max(0, y - expand_h)
    new_w = min(img_w - new_x, w + 2 * expand_w)
    new_h = min(img_h - new_y, h + 2 * expand_h)
    return new_x, new_y, new_w, new_h


def save_tiles(
    image: np.ndarray,
    boxes,
    output_dir: Path,
    resize_to=(154, 213),
    canvas_size=(205, 263),
    labels: Optional[List[str]] = None,
):
    """Crop, optionally resize, pad with black border, and save the tile images."""

    output_dir.mkdir(parents=True, exist_ok=True)
    img_h_total, img_w_total = image.shape[:2]
    for idx, (x, y, w, h) in enumerate(boxes):
        # Optionally expand bounding box before cropping
        x, y, w, h = _expand_box(x, y, w, h, save_tiles.bbox_margin, img_w_total, img_h_total)
        crop = image[y : y + h, x : x + w]
        if resize_to:
            crop = cv2.resize(crop, resize_to, interpolation=cv2.INTER_AREA)

        if canvas_size:
            crop = _pad_to_canvas(crop, canvas_size)

        # Determine filename
        if labels and idx < len(labels):
            label = labels[idx]
            # Sanitize label for filename (letters, digits, underscore)
            safe_label = (
                label.lower()
                .replace(" ", "_")
                .replace("/", "_")
                .replace("\\", "_")
            )
            filename = output_dir / f"letter_{safe_label}.png"
        else:
            filename = output_dir / f"tile_{idx + 1:02d}.png"
        cv2.imwrite(str(filename), crop)
    print(f"Saved {len(boxes)} tiles to {output_dir}")

# attach default attribute for closure-style config
save_tiles.bbox_margin = 0.0


def main():
    parser = argparse.ArgumentParser(
        description="Split a Wheel-of-Fortune style board (11×3) into 33 equally sized tile images."
    )
    parser.add_argument("input", type=Path, help="Path to the board image (e.g. letters.png)")
    parser.add_argument(
        "-o", "--output-dir", type=Path, default=Path("tiles"), help="Directory to write tile images"
    )
    parser.add_argument("--width", type=int, default=154, help="Inner (tile) width in pixels")
    parser.add_argument("--height", type=int, default=213, help="Inner (tile) height in pixels")
    parser.add_argument(
        "--canvas-width",
        type=int,
        default=205,
        help="Final canvas width after adding black border (default: 205)",
    )
    parser.add_argument(
        "--canvas-height",
        type=int,
        default=263,
        help="Final canvas height after adding black border (default: 263)",
    )
    parser.add_argument(
        "--labels",
        type=str,
        help=(
            "String or path to text file containing 33 labels in reading order (top-left "
            "to bottom-right). If the content contains the separator character (see "
            "--label-sep) or newlines, those tokens are used verbatim for filenames. "
            "Otherwise each character is treated as a single-letter label."
        ),
    )
    parser.add_argument(
        "--label-sep",
        type=str,
        default=",",
        help="Separator character used when splitting labels string/file (default: ',')",
    )
    parser.add_argument(
        "--bbox-margin",
        type=float,
        default=0.0,
        help="Fractional margin to expand each detected bounding box before cropping (e.g. 0.05 adds 5% on all sides).",
    )
    args = parser.parse_args()

    image = cv2.imread(str(args.input))
    if image is None:
        raise FileNotFoundError(f"Could not open image: {args.input}")

    boxes = find_tile_contours(image)
    if len(boxes) != 33:
        print(
            f"Warning: Expected 33 tiles but detected {len(boxes)}. Proceeding with what was found."
        )
    # Prepare labels list if provided
    labels_list: Optional[List[str]] = None
    if args.labels:
        label_source = Path(args.labels)
        if label_source.exists():
            labels_text = label_source.read_text().strip()
        else:
            labels_text = args.labels.strip()

        # Decide how to split: newline or custom separator means multi-token list
        if "\n" in labels_text or args.label_sep in labels_text:
            # Split by either newline or separator, ignoring empty tokens
            parts = re.split(r"[\n{}]".format(re.escape(args.label_sep)), labels_text)
            labels_list = [p.strip() for p in parts if p.strip()]
        else:
            # Fallback: treat every character as separate label
            labels_list = list(labels_text)

    # Set global margin for save_tiles helper
    save_tiles.bbox_margin = max(0.0, args.bbox_margin)

    save_tiles(
        image,
        boxes,
        args.output_dir,
        resize_to=(args.width, args.height),
        canvas_size=(args.canvas_width, args.canvas_height),
        labels=labels_list,
    )


if __name__ == "__main__":
    main() 