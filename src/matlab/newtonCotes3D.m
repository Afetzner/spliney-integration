function vols = newtonCotes3D(data, samples, distance)
    cotesCoefficients = [1 4 1 0 0 0 0; 1 3 3 1 0 0 0; 7 32 12 32 7 0 0; 19 75 50 50 75 19 0; 41 216 27 272 27 216 41];
    cotesCoefficients(3,:) =  cotesCoefficients(3,:) / 7;
    cotesCoefficients(4,:) = cotesCoefficients(4,:) / 19;
    cotesCoefficients(5,:) = cotesCoefficients(5,:) / 41;
    cof = ones(samples);
    templateRow = ones(samples, 1);
    templateRow(2:1:samples-1) = 2;
    cof(1,:) = templateRow;
    cof(:,1) = templateRow';
    cof(samples,:) = templateRow;
    cof(:,samples) = templateRow';
    cof = fillMatrix(cof);
    totalMat = cof.*data;
    mFactor = (1/2)^2;
    vols = [];
    vols (1, 1) = 1;
    vols (1, 2) = distance^2 * mFactor *  sum(totalMat, 'all');
    if (mod(samples, 2) == 1)
        templateRow = ones(samples, 1);
        templateRow(3:2:samples-2) = 2;
        templateRow(2:2:samples-1) = 4;
        cof(1,:) = templateRow;
        cof(:,1) = templateRow';
        cof(samples,:) = templateRow;
        cof(:,samples) = templateRow';
        cof = fillMatrix(cof);
        mFactor = (1/3)^2;
        totalMat = cof.*data;
        vols (end + 1, :) = [2, (distance^2 * mFactor *  sum(totalMat, 'all'))];
    end
    if (mod(samples, 3) == 1)
        templateRow = ones(samples, 1);
        templateRow(4:3:samples-1) = 2;
        templateRow(2:3:samples-1) = 3;
        templateRow(3:3:samples-1) = 3;
        cof(1,:) = templateRow;
        cof(:,1) = templateRow';
        cof(samples,:) = templateRow;
        cof(:,samples) = templateRow';
        cof = fillMatrix(cof);
        mFactor = (3/8)^2;
        totalMat = cof.*data;
        vols (end + 1, :) = [3, (distance^2 * mFactor *  sum(totalMat, 'all'))];
    end
    if (mod(samples, 4) == 1)
        templateRow = cotesCoefficients(3,1) * ones(samples, 1);
        templateRow(2:4:samples-1) = cotesCoefficients(3,2);
        templateRow(3:4:samples-1) = cotesCoefficients(3,3);
        templateRow(4:4:samples-1) = cotesCoefficients(3,2);
        templateRow(5:4:samples-1) = cotesCoefficients(3,1) * 2;
        cof(1,:) = templateRow;
        cof(:,1) = templateRow';
        cof(samples,:) = templateRow;
        cof(:,samples) = templateRow';
        cof = fillMatrix(cof);
        mFactor = (28/90)^2;
        totalMat = cof.*data;
        vols (end + 1, :) = [4, (distance^2 * mFactor *  sum(totalMat, 'all'))];
    end
    if (mod(samples, 5) == 1)
        templateRow = cotesCoefficients(4,1) * ones(samples, 1);
        templateRow(2:5:samples-1) = cotesCoefficients(4,2);
        templateRow(3:5:samples-1) = cotesCoefficients(4,3);
        templateRow(4:5:samples-1) = cotesCoefficients(4,3);
        templateRow(5:5:samples-1) = cotesCoefficients(4,2);
        templateRow(6:5:samples-1) = cotesCoefficients(4,1) * 2;
        cof(1,:) = templateRow;
        cof(:,1) = templateRow';
        cof(samples,:) = templateRow;
        cof(:,samples) = templateRow';
        cof = fillMatrix(cof);
        mFactor = (19 * 5/288)^2;
        totalMat = cof.*data;
        vols (end + 1, :) = [5, (distance^2 * mFactor *  sum(totalMat, 'all'))];
    end
    if (mod(samples, 6) == 1)
        templateRow = cotesCoefficients(5,1) * ones(samples, 1);
        templateRow(2:6:samples-1) = cotesCoefficients(5,2);
        templateRow(3:6:samples-1) = cotesCoefficients(5,3);
        templateRow(4:6:samples-1) = cotesCoefficients(5,4);
        templateRow(5:6:samples-1) = cotesCoefficients(5,3);
        templateRow(6:6:samples-1) = cotesCoefficients(5,2);
        templateRow(7:6:samples-1) = cotesCoefficients(5,1) * 2;
        cof(1,:) = templateRow;
        cof(:,1) = templateRow';
        cof(samples,:) = templateRow;
        cof(:,samples) = templateRow';
        cof = fillMatrix(cof);
        mFactor = (41 * 1/140)^2;
        totalMat = cof.*data;
        vols (end + 1, :) = [6, (distance^2 * mFactor *  sum(totalMat, 'all'))];
    end
end