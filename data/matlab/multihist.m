% list all filenames here. Use below
raw_folkwiki = "raw_folkwiki";
raw_sessions = "raw_sessions";
raw_folk_and_sess = "raw_folk_and_sess";

bob_lstm = "lstm_dropout-9_nov_folkwiki";
bob_gru = "gru_dropout-9_nov_folkwiki";

lstm_no_drop = "lstm_pretrain_dropout_folk_and_sess";
lstm_drop = "lstm_pretrain_no_dropout_folk_and_sess";

gru_no_drop = "gru_pretrain_no_dropout_folk_and_sess";
gru_drop = "gru_pretrain_dropout_folk_and_sess";

% specify which data files are to be included
figure_save_name = 'all_big_models';
data_cluster = [raw_folkwiki lstm_no_drop lstm_drop bob_lstm gru_no_drop gru_drop bob_gru];
figure_names = ["folkwiki"; "LSTM (0.0)"; "LSTM (0.5)"; "LSTM bob"; "GRU (0.0)"; "GRU (0.5)"; "GRU bob"];
normalize = true;

% load mat file as specified
data = [];
for i = 1:numel(data_cluster)
    strct = load(strcat(data_cluster(i), ".mat"));
    if normalize
        strct.keys_v = double(strct.keys_v)./double(sum(strct.keys_v));
        strct.metrics_v = double(strct.metrics_v)./double(sum(strct.metrics_v));
        strct.token_v = double(strct.token_v)./double(sum(strct.token_v));
    end
    data = [data; strct];
end


% plot dimensions
xoff = 0;
yoff = 0;
width = xoff + 91 * 3;
height = yoff + 130*2 * 3;

% plot keys
plot_multihist({data.keys_l}, {data.keys_v}, [yoff xoff height width], 0.5, strcat(figure_save_name, '_keys'), figure_names);

% plot metrics
plot_multihist({data.metrics_l}, {data.metrics_v}, [xoff+width yoff height width], 0.25, strcat(figure_save_name, '_metrics'), figure_names);

% plot token families
plot_multihist({data.token_l}, {data.token_v}, [xoff+width*2 yoff height width], 0.25, strcat(figure_save_name, '_tokens'), figure_names);