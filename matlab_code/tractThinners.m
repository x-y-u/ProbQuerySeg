function tractThinners(finput,foutput,options)
    %{
    ░█▀▀█ ░█▀▀▀█ ░█▀▄▀█ ░█▀▀▀ ░█▀▀▄ ▀█▀
    ░█─── ░█──░█ ░█░█░█ ░█▀▀▀ ░█─░█ ░█─
    ░█▄▄█ ░█▄▄▄█ ░█──░█ ░█▄▄▄ ░█▄▄▀ ▄█▄

    automated white matter tract thinners

        Created by Ye Wu, PhD (dr.yewu@outlook.com)

        - Nanjing University of Science and Technology
        - University of North Carolina at Chapel Hill

        Wu, Y., Hong, Y., Ahmad, S., Lin, W., Shen, D., Yap, P. T. (2020)
        Tract dictionary learning for fast and robust recognition of fiber bundles. 
        International Conference on Medical Image Computing and Computer-Assisted Intervention
        
    %}

    arguments
        finput  string {mustBeFile}
        foutput string
        
        options.minlength       (1,1)       {mustBeNonnegative} = 0
        options.maxlength       (1,1)       {mustBeNonnegative} = inf
        options.numcluster      (1,1)       {mustBeInteger,mustBeNonnegative} = 1
        options.threshold       (1,1)       {mustBeNumeric} = 0
        options.order           (1,1)       {mustBeInteger,mustBeNonnegative} = 4
        options.core            (1,1)       {mustBeInteger,mustBeNonnegative} = 2
    end
    
    assert(exist(finput,'file'),'Input file %s does not exist', finput);
    folder = fileparts(which(mfilename));
    addpath(fullfile(folder,'io'));

    % load tract
    tck = read_mrtrix_tracks(finput);
    tract = tck.data;

    % filtering with fiber lenth
    if options.minlength > 0 || ~isinf(options.maxlength)
        fiberLength = cellfun(@(x)sum(vecnorm(diff(x),2,2)),tract);

        tract = tract(fiberLength>=options.minlength & fiberLength<=options.maxlength);
    end

    % encoding in cosine space
    coef = fibencoding(tract,options.order,options.core);

    % quick clustering
    [~,~,~,D1] = kmedoids(coef',options.numcluster,'Distance', 'sqEuclidean','Replicates',2);

    coef(options.order*2+3,:) = [];
    coef(options.order+2,:) = [];
    coef(1,:) = [];

    [~,~,~,D2] = kmedoids(coef',options.numcluster,'Distance', 'sqEuclidean','Replicates',2);

    Z1 = zscore(min(D1,[],2));
    Z2 = zscore(min(D2,[],2));
    
    % statistical thresholding via zscore
    ind = Z1<=options.threshold & Z2<=options.threshold;
    tract = tract(ind);
    fprintf('%s: Removed streamline %4.2f percent \n',datetime('now'),100*sum(ind)/length(ind));

    tck.data = tract;
    tck.count = length(tract);
    write_mrtrix_tracks(tck,foutput);
end

function data = fibencoding(tract,order,core)
    nfib = length(tract);
    m = (order+1)*3;
    data = single(zeros(m,nfib));
    
    parfor (idx = 1:nfib, core)
        fib = tract{idx};
        len = max(size(fib));
        lmax = min(len,order);
    
        if max(size(fib)) < 3
            continue
        end
    
        fib(isnan(fib)|isinf(fib)) = 0;
    
        if isequal(size(fib,1),3)
            fib = fib';
        end
    
        [~,para] = parameterize_arclength(fib');
        try
            [~,X] = WFS_tracts(fib',para,lmax);
            data(:,idx) = [reshape(X,(lmax+1)*3,1);zeros(m-(lmax+1)*3,1)];
        catch
            continue;
        end
    end
end

function [arc_length,para]=parameterize_arclength(tract)
% (C) Moo K. Chung & Nagesh Adluru 2008
%     mkchung@wisc.edu
%     University of Wisconsin-Madison

n_vertex=size(tract,2);

p0=tract(:,1:(n_vertex-1));
p1=tract(:,2:n_vertex);
disp=p1-p0;
L2=sqrt(sum(disp'.^2,2));

arc_length=sum(L2);
cum_len=cumsum(L2)/arc_length;
para=zeros(1,n_vertex);
para(2:end)=cum_len';
end

function [wfs,beta]=WFS_tracts(tract,para,k)
% (C) Moo K. Chung & Nagesh Adluru 2008
%     mkchung@wisc.edu
%     University of Wisconsin-Madison

n_vertex=length(para);
para_even=[-para(n_vertex:-1:2) para];
tract_even=[tract(:,n_vertex:-1:2) tract];

Y=zeros(2*n_vertex-1,k+1);
para_even=repmat(para_even',1,k+1);
pi_factors=repmat([0:k],2*n_vertex-1,1).*pi;
Y=cos(para_even.*pi_factors).*sqrt(2);

beta=pinv(Y'*Y)*Y'*tract_even';

hat= Y*beta;

wfs=hat(n_vertex:(n_vertex*2-1),:);
end





