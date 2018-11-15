% list all filenames here. Use below
raw_folkwiki = 'raw_folkwiki';
raw_sessions = 'raw_sessions';
raw_folk_and_sess = 'raw_folk_and_sess';

bob_lstm = 'lstm_dropout-9_nov_folkwiki';
bob_gru = 'gru_dropout-9_nov_folkwiki';

% load mat file as specified
figure_save_name = raw_folk_and_sess;
data = load(strcat(figure_save_name, '.mat'));

% plot dimensions
xoff = 0;
yoff = 0;
width = xoff + 91 * 4;
height = yoff + 130 * 4;

% plot keys
plot_hist(data.keys_l, data.keys_v, [yoff xoff height width], strcat(figure_save_name, '_keys'), 0.5);

% plot metrics
plot_hist(data.metrics_l, data.metrics_v, [xoff+width yoff height width], strcat(figure_save_name, '_metrics'), 0.25);

% plot token families
plot_hist(data.token_l, data.token_v, [xoff+width*2 yoff height width], strcat(figure_save_name, '_tokens'), 0.125);