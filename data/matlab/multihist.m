% list all filenames here. Use below
raw_folkwiki = "data/folkwiki";

bob_lstm = "data/lstm_bob";
bob_gru = "data/gru_bob";

lstm_no_drop = "data/lstm_pretrain_dropout";
lstm_drop = "data/lstm_pretrain_no_dropout";

gru_no_drop = "data/gru_pretrain_no_dropout";
gru_drop = "data/gru_pretrain_dropout";

gru_no_drop_new = "data/gru_pretrain_no_dropout_new";
gru_drop_new = "data/gru_pretrain_dropout_new";

gru_no_drop_new_30 = "data/gru_pretrain_no_dropout_30";
gru_drop_new_30 = "data/gru_pretrain_dropout_30";


% specify which data files are to be included
%figure_save_name = 'pretrain_dropout_models_and_folkwiki_small';
figure_save_name = 'GRU_old_new_comparison';
data_cluster = [raw_folkwiki gru_drop_new_30 gru_no_drop_new_30 gru_drop gru_no_drop];
figure_names = ["folkwiki"; "GRU (50% dropout)"; "GRU (0% dropout)"; "GRU (50% dropout) Overfitted"; "GRU (0% dropout) Overfitted"];
normalize = true;


% load mat file as specified
data = [];
for i = 1:numel(data_cluster)
    strct = load(strcat(data_cluster(i), ".mat"));
    if normalize
        strct.keys_v = double(strct.keys_v)./double(sum(strct.keys_v)) * 100;
        strct.metrics_v = double(strct.metrics_v)./double(sum(strct.metrics_v)) * 100;
        strct.token_v = double(strct.token_v)./double(sum(strct.token_v)) * 100;
        strct.note_v = double(strct.note_v)./double(sum(strct.note_v)) *100;
    end
    data = [data; strct];
end

% plot dimensions
xoff = 0;
yoff = 0;
%width = xoff + 91 * 1.8;
%height = yoff + 130*2 * 1.8;
width = xoff + 91 * 3;
height = yoff + 130 * 2 * 3;


% plot keys
plot_multihist({data.keys_l}, {data.keys_v}, [yoff xoff height width+20], 0.25, strcat(figure_save_name, '_keys'), figure_names, 'Key', 'northwest', [0:5:25], -2);

% plot metrics
plot_multihist({data.metrics_l}, {data.metrics_v}, [xoff+width yoff height width], 0.25, strcat(figure_save_name, '_metrics'), figure_names, 'Meter', 'northeast', [0:20:90], -8);

% plot token families
%plot_multihist({data.note_l}, {data.note_v}, [xoff+width*2 yoff height width], 0.25, strcat(figure_save_name, '_notes'), figure_names);

% plot token families
plot_multihist2({data.count_l}, {data.count_v}, [xoff+width*3 yoff height width], -0, strcat(figure_save_name, '_count'), figure_names, [0:10:30], -4);