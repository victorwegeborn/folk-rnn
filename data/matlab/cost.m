
data = {
    'lstm pretrain', load('cost/lstm_pretrain_training.txt'); % 1
    'lstm pretrain valid', load('cost/lstm_pretrain_validation.txt'); % 2

    'lstm drop', load('cost/lstm_dropout_training.txt'); % 3
    'lstm drop valid', load('cost/lstm_dropout_validation.txt'); % 4

    'lstm no drop', load('cost/lstm_no_dropout_training.txt'); % 5
    'lstm no drop valid', load('cost/lstm_no_dropout_validation.txt'); % 6

    'gru pretrain', load('cost/gru_pretrain_training.txt'); % 7 
    'gru pretrain valid', load('cost/gru_pretrain_validation.txt'); % 8 

    'gru drop', load('cost/gru_dropout_training.txt'); % 9
    'gru drop valid', load('cost/gru_dropout_validation.txt'); % 10

    'gru no drop', load('cost/gru_no_dropout_training.txt'); % 11
    'gru no drop valid', load('cost/gru_no_dropout_validation.txt') % 12
};


idx = [1, 3, 5, 7, 9, 11];

for j = 1:numel(idx)
    i = idx(j);
    subplot(2,1,1);
    plot(data{i,2});
    title(data{i,1});

    subplot(2,1,2);
    plot(data{i+1,2});
    title(data{i+1,1});

    saveas(gca, strcat('./cost_figs/', data{i,1}, '.png'));
end


