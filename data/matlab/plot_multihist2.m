function [] = plot_multihist2( labels, values, size_, offset, filename, cluster, yaxel, yoff)
    
    
    N = 0;
    n_cells = length(values);
    
    
    % find longest array
    for i = 1:n_cells
        N = max(N, max(labels{i}(1,:)));
    end

    bucket_size = 50;
    nbuckets = ceil(N/bucket_size);

    % set bucket
    new_values = {};
    for i = 1:n_cells
        bucket = zeros(1, nbuckets + 1);
        for j = 1:length(labels{i}(1,:))
            idx = labels{i}(1,j);
            bucket_idx = ceil(idx/bucket_size) + 1;
            bucket(1, bucket_idx) = bucket(1, bucket_idx) + values{i}(1,j);
        end
        new_values{i} = bucket./double(sum(bucket))*100;
        mean(bucket);
    end
    
    v = [new_values{:}]';
    new_values = reshape(v, [length(new_values{1}), length(new_values)]);

    
    
    cm = [0 0 0; 0.5 0.5 0.5; 0.76 0.76 0.76];
    
    nbuckets = 10;
    
    figure('rend','painters','pos', size_);
    bar(new_values, 'EdgeColor', 'None', 'BarWidth', 1);
    key_ticks = (1:nbuckets);
    xlim([0.5 nbuckets+1]);
    xticks(key_ticks-0.20);
    yticks(yaxel)
    ax = gca;
    ax.TickLength = [0 4];
    ax.YGrid = 'on';
    ax.GridLineStyle = '-';
    ax.GridAlpha = 0.5;
    xtickangle(70);
    xticklabels(key_ticks*bucket_size);
    set(gca,'FontSize',14);
    colormap(ax,rgb2gray(cm));
    legend(cluster,'Orientation','vertical','Location','northeast');
    y = ylabel('% of transcriptions');
    xlabel('Number of tokens');
    
    
    ax = gca;
    outerpos = ax.OuterPosition;
    ti = ax.TightInset;
    left = outerpos(1) + ti(1);
    bottom = outerpos(2) + ti(2);
    ax_width = outerpos(3) - ti(1) - ti(3)-0.01;
    ax_height = outerpos(4) - ti(2) - ti(4);
    ax.Position = [left bottom ax_width ax_height];
    set(gca,'color','none');
    
    ypos = y.Position + ([0 yoff 0]);
    set(y, 'Position', ypos);
    
    saveas(gca, strcat('./figures/', filename, '.png'));
    
end

