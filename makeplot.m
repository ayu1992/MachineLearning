d = importdata('diff_neighbor');
L = length(d);
hist(d)
ylabels = get(gca, 'YTickLabel');
ylabels = linspace(0, str2num(ylabels(length(ylabels),:))/L,length(ylabels));
set(gca,'YTickLabel',ylabels);
xlabel('r - r_{hat}');
ylabel('P');
title('Histogram of prediction errors in neighborhood model using my formulation');