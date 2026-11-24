import argparse
from collections import Counter
from pathlib import Path
import cv2
import numpy as np

# run 
# python bellara_scanner.py image2.png --first L

# by default 19
lines_for_scanning = 90


SIZES = {'S': 90, 'M': 135, 'L': 200}
LABELS = np.array(list(SIZES))
MM = np.array(list(SIZES.values()))


def runs(mask):
    return np.flatnonzero(np.diff(np.r_[False, mask, False])).reshape(-1, 2)


def scan(path, first=None, output=None):
    image = cv2.imread(str(path))
    if image is None:
        raise ValueError('Cannot open image')
    h, w = image.shape[:2]
    gray = cv2.GaussianBlur(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (5, 5), 0)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    pink = cv2.inRange(hsv, (135, 70, 50), (179, 255, 255)) > 0
    samples = []
    for y in np.linspace(h * .1, h * .9, lines_for_scanning).astype(int):
        lo, hi = max(0, y-3), min(h, y+4)
        profile = np.median(gray[lo:hi], axis=0)
        # Local background makes threshold less sensitive to lighting.
        k = max(15, (w // 35) | 1)
        background = cv2.dilate(profile.astype(np.float32)[None, :], np.ones((1,k), np.uint8))[0]
        dark = (profile < .60 * background) & (profile < 125)
        bars = runs(dark)
        bars = bars[(bars[:,1]-bars[:,0]) >= max(2, round(w*.0015))]
        starts = runs(pink[lo:hi].mean(axis=0) > .5)
        if not len(starts):
            continue
        start = max(starts, key=lambda p: p[1]-p[0])
        bars = bars[bars[:,0] > start[1]]
        if len(bars) < 3:
            continue
        thickness = np.median(np.diff(bars, axis=1))
        centers = bars.mean(axis=1)
        # Use the inner edge of a thick terminal frame, not its center.
        if bars[-1,1]-bars[-1,0] > 1.7*thickness:
            centers[-1] = bars[-1,0] + thickness/2
        samples.append((y, np.r_[start.mean(), centers]))
    if not samples:
        raise ValueError('No pink start / usable separators found')
    count, votes = Counter(len(x) for _,x in samples).most_common(1)[0]
    selected = [(y,x) for y,x in samples if len(x)==count]
    if votes < 10:
        raise ValueError(f'Inconsistent separator count: {votes}/19 scan lines')
    positions = np.array([x for _,x in selected])
    widths = np.median(np.diff(positions, axis=1), axis=0)
    interior = widths[1:-1]
    if len(interior)<2:
        raise ValueError('Too few interior panels for scale estimation')
    # Fit scale to known widths; do not assume an S panel exists.
    candidates = (interior[:,None]/MM).ravel()
    def cost(scale):
        errors = np.min(abs(interior[:,None]/(scale*MM)-1), axis=1)
        return np.mean(np.minimum(errors,.35))
    scale = min(candidates, key=cost)
    idx = np.argmin(abs(interior[:,None]/(scale*MM)-1), axis=1)
    scale = np.median(interior/MM[idx])
    if len(set(idx))<2:
        raise ValueError('Scale ambiguous: need multiple sizes or external calibration')
    # Allow a gradual scale drift across the image (mild perspective).
    x = np.arange(len(widths), dtype=float)
    local = interior/MM[idx]
    slope, intercept = np.polyfit(x[1:-1], local, 1)
    scales = np.clip(intercept+slope*x, .8*scale, 1.2*scale)
    errors = abs(widths[:,None]/(scales[:,None]*MM)-1)
    best = errors.argmin(axis=1)
    labels = [str(LABELS[j]) if errors[i,j] <= .12 else '?' for i,j in enumerate(best)]
    if first:
        labels[0] = first
    # An edge may be cropped even if its width resembles a valid size.
    # Always require a human check of the first panel.
    if not first:
        labels[0] = '?'
    overlay = image.copy()
    top, bottom = positions[0], positions[-1]
    yt, yb = selected[0][0], selected[-1][0]
    for a,b in zip(top,bottom):
        cv2.line(overlay,(round(a),yt),(round(b),yb),(0,220,0),2)
    middle = np.median(positions,axis=0)
    for i,label in enumerate(labels):
        cx = int((middle[i]+middle[i+1])/2)
        color = (0,165,255) if label=='?' or (i==0 and first) else (0,220,0)
        cv2.rectangle(overlay,(cx-17,h//2-22),(cx+17,h//2+22),(25,25,25),-1)
        cv2.putText(overlay,label,(cx-12,h//2+12),cv2.FONT_HERSHEY_SIMPLEX,1.1,color,2,cv2.LINE_AA)
    if output is None:
        output = Path(path).with_name(Path(path).stem+'_marked.png')
    if not cv2.imwrite(str(output),overlay):
        raise ValueError('Cannot write output')
    return {'sequence': ''.join(labels), 'counts': dict(Counter(labels)), 'widths_px': np.round(widths,1).tolist(), 'scan_lines': votes, 'first_manual': first, 'output': str(output)}

# Start the script if run directly
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image')
    parser.add_argument('--first', choices=SIZES, help='Manually confirmed first panel')
    parser.add_argument('--output')
    args = parser.parse_args()
    result = scan(args.image, args.first, args.output)
    for key,value in result.items():
        print(f'{key}: {value}')
