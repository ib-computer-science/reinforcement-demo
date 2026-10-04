unitsize(1cm);

// Rounded-rectangle helper: corners are true quarter-circle arcs, which holds
// up correctly even for short/wide rectangles (unlike direction-constrained
// Bezier corners, which can overshoot at extreme aspect ratios).
path roundedrect(pair a, pair b, real r) {
    return
        (a.x + r, a.y)--(b.x - r, a.y)--arc((b.x - r, a.y + r), r, -90, 0)
        --(b.x, b.y - r)--arc((b.x - r, b.y - r), r, 0, 90)
        --(a.x + r, b.y)--arc((a.x + r, b.y - r), r, 90, 180)
        --(a.x, a.y + r)--arc((a.x + r, a.y + r), r, 180, 270)
        --cycle;
}

pen cabinetRed = rgb(0.80, 0.16, 0.16);
pen cabinetDark = rgb(0.45, 0.06, 0.06);
pen gold = rgb(0.95, 0.75, 0.15);
pen goldDark = rgb(0.72, 0.52, 0.05);
pen screenNavy = rgb(0.10, 0.12, 0.25);

pen backgroundColor = black;   // fill behind the whole drawing; override before including this file

// --- background ---
fill((-5.5, -7)--(5.5, -7)--(5.5, 6)--(-5.5, 6)--cycle, backgroundColor);

// --- legs ---
filldraw(roundedrect((-2.3, -6.3), (-1.5, -5.3), 0.15), cabinetDark, black + linewidth(1));
filldraw(roundedrect((1.5, -6.3), (2.3, -5.3), 0.15), cabinetDark, black + linewidth(1));

// --- left arm (lever) ---
draw((-3.3, 1.5)--(-4.3, 4.8), cabinetDark + linewidth(4));
filldraw(circle((-3.3, 1.5), 0.25), cabinetDark, black + linewidth(1));
filldraw(circle((-4.3, 4.8), 0.55), gold, goldDark + linewidth(1.5));

// --- right arm (lever) ---
draw((3.3, 1.5)--(4.3, 4.8), cabinetDark + linewidth(4));
filldraw(circle((3.3, 1.5), 0.25), cabinetDark, black + linewidth(1));
filldraw(circle((4.3, 4.8), 0.55), gold, goldDark + linewidth(1.5));

// --- main cabinet body ---
filldraw(roundedrect((-3, -5.3), (3, 3), 0.5), cabinetRed, black + linewidth(2));

// --- mask cord: continues from the band's sides and disappears behind the
//     cabinet's edge, as if tied around the back ---
draw((-2.4, 1.15)--(-3, 1.15), black + linewidth(4));
draw((2.4, 1.15)--(3, 1.15), black + linewidth(4));

// --- face: eye mask band ---
filldraw((-2.4, 1.55)--(2.4, 1.55)--(2.4, 0.75)--(-2.4, 0.75)--cycle, black, black);

// --- eyes (white with black pupils), peeking over the mask edge ---
filldraw(circle((-1.1, 1.15), 0.42), white, black + linewidth(1.5));
filldraw(circle((1.1, 1.15), 0.42), white, black + linewidth(1.5));
filldraw(circle((-1.0, 1.15), 0.17), black, black);
filldraw(circle((1.0, 1.15), 0.17), black, black);

// --- sly cartoon grin ---
draw((-0.9, 0.2)..(0, -0.15)..(0.9, 0.2), black + linewidth(2.5));

// --- screen with two reels, each showing both of its possible outcomes ---
filldraw(roundedrect((-2.4, -3.6), (2.4, -0.4), 0.3), screenNavy, black + linewidth(1.5));

pen reelGray = rgb(0.75, 0.75, 0.75);

// A reel is a pill-shaped drum split into a "win" face (top) and a "lose"
// face (bottom) by a dividing line, with faint curved bands hinting that
// it's a revolving cylinder rather than a flat window.
void drawReel(pair c, real w, real h) {
    path shell = roundedrect(c - (w / 2, h / 2), c + (w / 2, h / 2), w / 2);
    filldraw(shell, white, black + linewidth(1.2));
    draw((c.x - w / 2 + 0.05, c.y)--(c.x + w / 2 - 0.05, c.y), gray(0.4) + linewidth(1));
    draw((c.x - w / 2 + 0.1, c.y + h / 4)..(c.x, c.y + h / 4 - 0.06)..(c.x + w / 2 - 0.1, c.y + h / 4), reelGray + linewidth(0.7));
    draw((c.x - w / 2 + 0.1, c.y - h / 4)..(c.x, c.y - h / 4 - 0.06)..(c.x + w / 2 - 0.1, c.y - h / 4), reelGray + linewidth(0.7));
}

real reelW = 1.3;
real reelH = 2.0;
pair leftReel = (-1.1, -2);
pair rightReel = (1.1, -2);

drawReel(leftReel, reelW, reelH);
drawReel(rightReel, reelW, reelH);

// win faces, top half: the same symbol on both reels, since a "win" is the
// same kind of outcome on either arm — only its probability differs
filldraw(circle(leftReel + (0, reelH / 4), 0.32), gold, goldDark + linewidth(0.8));
label("$\$$", leftReel + (0, reelH / 4), fontsize(11pt) + goldDark);
filldraw(circle(rightReel + (0, reelH / 4), 0.32), gold, goldDark + linewidth(0.8));
label("$\$$", rightReel + (0, reelH / 4), fontsize(11pt) + goldDark);

// lose faces, bottom half: muted and blank
filldraw(circle(leftReel - (0, reelH / 4), 0.28), reelGray, gray(0.4) + linewidth(0.8));
filldraw(circle(rightReel - (0, reelH / 4), 0.28), reelGray, gray(0.4) + linewidth(0.8));

// --- coin slot ---
filldraw(roundedrect((-0.5, -4.6), (0.5, -4.2), 0.1), screenNavy, black + linewidth(1));

// --- sparkle decorations ---
path sparkle(pair c, real s) {
    return (c + s * dir(90))--(c + 0.3 * s * dir(0))--(c + s * dir(270))--(c + 0.3 * s * dir(180))--cycle;
}
fill(sparkle((-4.7, 2.2), 0.35), gold);
fill(sparkle((4.7, 2.2), 0.35), gold);
fill(sparkle((-4.2, -0.5), 0.22), gold);
fill(sparkle((4.2, -0.5), 0.22), gold);
