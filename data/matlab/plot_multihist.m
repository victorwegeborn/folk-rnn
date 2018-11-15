function [] = plot_multihist( labels, values, size_, offset, filename, cluster)
       

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
    
    v = [values{:}]';
    values = reshape(v, [length(values{1}), length(values)]);

    

   
    labels = new_labels;
    figure('rend','painters','pos', size_);
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
    set(gca,'FontSize',14)
    legend(cluster,'Orientation','horizontal','Location','northoutside');
    
    saveas(gca, strcat('./figures/', filename, '.png'));
    
end

