function [] = plot_hist( labels, values, size, filename, offset)

    f = figure('rend','painters','pos', size);
    bar(values);
    

    key_ticks = (1:length(labels));
    xlim([0 key_ticks(end)+1])
    xticks(key_ticks-offset);
    ax = gca;
    ax.TickLength = [0 0];
    ax.YGrid = 'on';
    ax.GridLineStyle = '-';
    xtickangle(70);
    xticklabels(labels);
    set(gca,'FontSize',16)
    
    saveas(gca, strcat('./figures/', filename, '.png'))
    
end

