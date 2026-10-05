import graph;

size(400, 250, IgnoreAspect);

pen bg = black;   // background fill; override before this point to change it
pen fg = white;   // axes, labels, and legend text/border

file in = input("q_learn_convergence.dat").line();
real[][] data = in.dimension(0, 0);
data = transpose(data);
real[] step = data[0];
real[] p_prev_l = data[1];
real[] p_prev_r = data[2];

// With epsilon = 0.1, a converged policy still explores both arms equally
// 10% of the time, so behaviour plateaus at 0.95 / 0.05 rather than 1.0 / 0.0.
real[] xref = {step[0], step[step.length - 1]};
real[] yref95 = {0.95, 0.95};
real[] yref05 = {0.05, 0.05};
draw(graph(xref, yref95), gray + dotted);
draw(graph(xref, yref05), gray + dotted);

// Red is drawn noticeably thicker than blue (a dashed stroke on this noisy, jittery
// data just looked like a broken mess) so the two curves stay distinguishable
// without relying on color, e.g. in black-and-white print.
draw(graph(step, p_prev_l), blue + linewidth(0.8), "$P(\mathrm{pull\ R} \mid \mathrm{prev}=\mathrm{L})$");
draw(graph(step, p_prev_r), red + linewidth(2.2), "$P(\mathrm{pull\ R} \mid \mathrm{prev}=\mathrm{R})$");

ylimits(0, 1);

xaxis("training step", BottomTop, LeftTicks, p=fg);
yaxis("P(pull R)", LeftRight, RightTicks, p=fg);

add(legend(p=fg), point(E), 20 * E, UnFill);

shipout(bbox(currentpicture, 3mm, p=bg, filltype=Fill));
