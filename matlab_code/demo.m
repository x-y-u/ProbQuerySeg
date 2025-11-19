clear all; clc;

% 根目录
rootDir = '/media/UG3/xieyu/fiber_query/HCPA/fiber_recognize_results';

% 获取所有样本目录
subjects = dir(fullfile(rootDir, '*'));
subjects = subjects([subjects.isdir]);

minlength_map = containers.Map( ...
    {'ATR_left.tck', 'ATR_right.tck', 'CA.tck', 'CC_1.tck', 'CC_5.tck', 'CC_6.tck', 'CG_left.tck', 'CG_right.tck', 'FX_left.tck', 'FX_right.tck', 'ICP_left.tck' ...
    , 'ICP_right.tck', 'MLF_left.tck', 'MLF_right.tck', 'SCP_left.tck', 'SCP_right.tck', 'SLF_I_left.tck', 'SLF_I_right.tck', 'SLF_III_left.tck', 'SLF_III_right.tck' ...
    , 'CST_left.tck', 'CST_right.tck', 'FPT_left.tck', 'FPT_right.tck', 'POPT_left.tck', 'POPT_right.tck'}, ...
    [35, 35, 25, 30, 25, 30, 30, 30, 10, 10, 10, 10, 25, 25, 25, 25, 25, 25, 25, 25, 45, 45, 45, 45, 45, 45] ...
);

for i = 1:length(subjects)
    subDir = fullfile(rootDir, subjects(i).name);
    outDir = fullfile(rootDir, subjects(i).name, 'fiber_query_results-track_ifod1_rk4_dynamic_1M-thined');
    if ~exist(outDir, 'dir')
        mkdir(outDir);
    end
    disp(['Processing ' subjects(i).name ' ...']);

    bundles = dir(fullfile(subDir, 'fiber_query_results-track_ifod1_rk4_dynamic_1M', '*.tck'));
    bundle_names = {bundles.name};

    for j = 1:length(bundle_names)
        bundle = bundle_names{j};
        finput  = fullfile(subDir, 'fiber_query_results-track_ifod1_rk4_dynamic_1M', bundle);
        foutput = fullfile(outDir, bundle);

        if isKey(minlength_map, bundle)
            minlen = minlength_map(bundle);
        elseif contains(bundle, 'ST')
            minlen = 25;
        elseif contains(bundle, 'T_')
            minlen = 35
        else
            minlen = 45;
        end

        if exist(finput, 'file')
            try
                tractThinners(finput, foutput, minlength=minlen, maxlength=240, threshold=0.5, order=4, numcluster=16);
                disp(['  Done: ' bundle]);
            catch ME
                warning(['  Error processing ' bundle ': ' ME.message]);
            end
        else
            warning(['  Missing file: ' finput]);
        end
        % break
    end
    % break
end

disp('All processing finished.');