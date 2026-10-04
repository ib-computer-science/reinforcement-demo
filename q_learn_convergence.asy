import graph;

size(400, 250, IgnoreAspect);

file in = input("q_learn_convergence.dat").line();
real[][] data = in.dimension(0, 0);
data = transpose(data);
real[] step = data[0];
real[] p_state0 = data[1];
real[] p_state1 = data[2];

// With epsilon = 0.1, a converged policy still explores both arms equally
// 10% of the time, so behaviour plateaus at 0.95 / 0.05 rather than 1.0 / 0.0.
real[] xref = {step[0], step[step.length - 1]};
real[] yref95 = {0.95, 0.95};
real[] yref05 = {0.05, 0.05};
draw(graph(xref, yref95), gray + dashed);
draw(graph(xref, yref05), gray + dashed);

draw(graph(step, p_state0), blue + linewidth(1.2), "$P(\mathrm{arm}=1 \mid \mathrm{state}=0)$");
draw(graph(step, p_state1), red + linewidth(1.2), "$P(\mathrm{arm}=1 \mid \mathrm{state}=1)$");

ylimits(0, 1);

xaxis("training step", BottomTop, LeftTicks);
yaxis("P(pull arm 1)", LeftRight, RightTicks);

add(legend(), point(E), 20 * E, UnFill);
