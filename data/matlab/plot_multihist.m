function [] = plot_multihist(labels, values, size_, offset, filename, cluster, x_label, loc, yaxle, yoff)
    
    

    lab = {};
    for i = 1:length(labels)
        l_c = labels{i};
        for j = 1:length(l_c)
            s = strtrim(l_c(j,:));
            if ~any(strcmp(lab, s))
                lab{end+1} = s;
            end
        end
    end
    new_labels = sort(lab);
    
    length(new_labels)
    for i = 1:length(values)
        old_values = values{i};
        new_values = zeros(1,length(new_labels));
        if length(old_values) == length(new_values)
            continue
        end
        for j = 1:length(new_labels)
            new_l = new_labels(j);
            new_l = new_l{1};
            old_labels = labels{i};
            for k = 1:length(old_labels)
                old_l = strtrim(old_labels(k,:));
                if strcmp(new_l, old_l)
                    new_values(j) = old_values(k);
                    continue
                end
            end
        end
        values{i} = new_values;
    end
 
   
    
    n_buckets = length(values);
    bucket_length = length(values{1});
    vals = cell(1, n_buckets);
    labs = cell(1);
    % filter out less then 1%
    if strcmp('Key', x_label)
        for i = 1:bucket_length
            p = 0;
            for j = 1:n_buckets
                p = p + values{j}(1,i);
            end
            
            if p >= double(n_buckets)
               for j = 1:n_buckets
                    vals{j}(1,i) = values{j}(1,i);
                    labs(1,i) = new_labels(1,i);
               end
            end
        end
    elseif strcmp('Meter', x_label)
        for i = 1:length(new_labels)
            new_labels(1,i);
            if any(strcmp({'2/2', '2/4', '3/4', '4/4', '6/8', '9/8'}, new_labels(1,i)))
                labs(1,i) = strtrim(new_labels(1,i));
                for j = 1:n_buckets
                    vals{j}(1,i) = values{j}(1,i);
                end
            end
        end

    end

    v = [vals{:}]';
    values = reshape(v, [length(vals{1}), length(vals)]);
    values( ~any(values,2), : ) = [];
    cm = [0 0 0; 0.54 0.54 0.54; 0.73 0.73 0.73];
    labels = labs;
    labels(cellfun('isempty', labels)) = [];
    figure('rend','painters','pos', size_);
    bar(values, 'EdgeColor', 'None', 'BarWidth', 1);
    key_ticks = (1:length(values));
    xlim([0 key_ticks(end)+1]);
    xticks(key_ticks-offset);
    yticks(yaxle)
    ax = gca;
    ax.TickLength = [0 0];
    ax.YGrid = 'on';
    ax.GridLineStyle = '-';
    ax.GridAlpha = 0.5;
    xtickangle(70);
    xticklabels(labels);
    set(gca,'FontSize',14);
    %colormap(ax,rgb2gray(cm));
    colormap(ax, parula);
    legend(cluster,'Orientation','vertical','Location',loc);
    
    y = ylabel('% of transcriptions');
    
    xlabel(x_label);
    
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

