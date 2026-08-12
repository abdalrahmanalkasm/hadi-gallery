/**
 * Turns the human-readable `dimensions` field ("120 × 90 cm") into the
 * numbers the layout needs. This is the mechanism behind the direction in
 * design-brief.md: one parsed number drives both the image width and the
 * length of its measure bar, so the two can never disagree.
 *
 * Why a square root and not a straight proportion:
 * the collection spans a 220 cm canvas down to a 10 cm panel, a 22:1
 * range. Mapping that linearly pins every study and most prints onto the
 * minimum width, so a 50 cm print ends up the same size as a 21 cm sketch
 * — which destroys exactly the comparison the design exists to make. The
 * square root keeps the ordering and the sense of "much larger", while
 * leaving the small work legible on a phone.
 *
 *   220 cm -> 100%    100 cm -> 67%     25 cm -> 34%
 *   180 cm ->  90%     50 cm -> 48%     10 cm -> 26% (floor)
 */

/** Largest work in the collection, in cm. Sets the 100% mark. */
export const MAX_CM = 220;

/** Floor, in percent. Below this the smallest studies stop being legible. */
export const MIN_PCT = 26;

/** "120 × 90 cm" -> 120 · handles ×, x and * */
export function widthCm(dimensions) {
  const m = String(dimensions).match(/([\d.]+)\s*[×x*]/i);
  return m ? parseFloat(m[1]) : null;
}

/** "120 × 90 cm" -> 90 */
export function heightCm(dimensions) {
  const m = String(dimensions).match(/[×x*]\s*([\d.]+)/i);
  return m ? parseFloat(m[1]) : null;
}

/** Percentage of the column this work should occupy. */
export function scalePct(dimensions) {
  const cm = widthCm(dimensions);
  if (!cm) return 100;
  const pct = Math.sqrt(Math.min(cm, MAX_CM) / MAX_CM) * 100;
  return Math.min(100, Math.max(MIN_PCT, pct));
}

/** Inline custom property consumed by `.work-scaled { width: var(--w) }` */
export function scaleStyle(dimensions) {
  return `--w: ${scalePct(dimensions).toFixed(1)}%`;
}

/** Track width for works laid out side by side (prints, studies). */
export function trackStyle(dimensions) {
  const pct = Math.min(100, scalePct(dimensions) * 1.06);
  return `flex-basis: ${pct.toFixed(1)}%`;
}
