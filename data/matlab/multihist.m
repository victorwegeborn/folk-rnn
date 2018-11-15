% list all filenames here. Use below
raw_folkwiki = "raw_folkwiki";
raw_sessions = "raw_sessions";
raw_folk_and_sess = "raw_folk_and_sess";

bob_lstm = "lstm_dropout-9_nov_folkwiki";
bob_gru = "gru_dropout-9_nov_folkwiki";

% specify which data files are to be included
figure_save_name = 'bob_summary';
data_cluster = [raw_folkwiki bob_lstm bob_gru];
figure_names = ["folkwiki"; "lstm"; "gru"];


% load mat file as specified
data = [];
for i = 1:numel(data_cluster)
    data = [data; load(strcat(data_cluster(i), ".mat"))];
end


% plot dimensions
xoff = 0;
yoff = 0;
width = xoff + 91 * 4;
height = yoff + 130 * 4;

% plot keys
plot_multihist({data.keys_l}, {data.keys_v}, [yoff xoff height width], 0.5, strcat(figure_save_name, '_keys'), figure_names);

% plot metrics
plot_multihist({data.metrics_l}, {data.metrics_v}, [xoff+width yoff height width], 0.25, strcat(figure_save_name, '_metrics'), figure_names);

% plot token families
plot_multihist({data.token_l}, {data.token_v}, [xoff+width*2 yoff height width], 0.25, strcat(figure_save_name, '_tokens'), figure_names);