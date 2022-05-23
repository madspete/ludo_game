clc;
clear;
close all;

%% Test difference between different training strategies
random_against_random = [71.0, 70.55, 72.25, 70.8, 72.39999999999999, 71.1, 71.6, 71.35000000000001, 70.7, 71.2];
random_against_ss = [48.15, 48.1, 48.699999999999996, 48.3, 46.85, 48.3, 47.5, 50.74999999999999, 48.3, 48.5];

ss_against_random = [69.39999999999999, 72.5, 72.2, 70.65, 71.85000000000001, 72.3, 72.2, 72.1, 72.6, 71.8];
ss_against_ss = [49.9, 49.55, 50.05, 49.6, 49.9, 49.5, 51.949999999999996, 48.6, 49.2, 49.35];

self_against_random = [71.7, 72.15, 69.55, 72.35000000000001, 71.3, 72.8, 72.15, 71.3, 70.5, 72.75];
self_against_ss = [49.05, 49.5, 50.0, 49.5, 49.6, 48.6, 48.449999999999996, 49.6, 48.4, 49.0];

random_test = [random_against_random' ss_against_random' self_against_random'];
ss_test = [random_against_ss' ss_against_ss' self_against_ss'];

figure("name", "random normallity")
subplot(2,1,1)
qqplot(random_against_random)
subplot(2,1,2)
qqplot(random_against_ss)

figure("name", "ss normallity")
subplot(2,1,1)
qqplot(ss_against_random)
subplot(2,1,2)
qqplot(ss_against_ss)

figure("name", "self normallity")
subplot(2,1,1)
qqplot(self_against_random)
subplot(2,1,2)
qqplot(self_against_ss)

% Test for equal variance
vartestn(random_test);
vartestn(ss_test);

% Test ANOVA
anova1(random_test);
anova1(ss_test);

% t-test for ss_test
bonf_corrected_p_value = 0.05/3;
[h,p] = ttest2(random_against_ss, ss_against_ss, "Alpha",bonf_corrected_p_value)
[h,p] = ttest2(random_against_ss, self_against_ss, "Alpha",bonf_corrected_p_value)
[h,p] = ttest2(ss_against_ss, self_against_ss, "Alpha",bonf_corrected_p_value)

