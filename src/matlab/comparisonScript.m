flatMatrixVols = newtonCotes3D(flatMat, samples, 1/(samples-1))
halfMatrixVols = newtonCotes3D(halfSlope, samples, 1/(samples-1))
bowlMatrixVols = newtonCotes3D(bowlShape, samples, 1/(samples-1))
bowl2MatrixVols = newtonCotes3D(bowlShape2, samples, 2/(samples-1))
cubicMatrixVols = newtonCotes3D(cubicShape, samples, 1/(samples-1))

flatMatrixVols(:,3) = flatMatrixVols(:,2) - 1;
halfMatrixVols(:,3) = halfMatrixVols(:,2) - (1/2);
bowlMatrixVols(:,3) = bowlMatrixVols(:,2) - (2/3);
bowl2MatrixVols(:,3) = bowl2MatrixVols(:,2) - (8/3);
cubicMatrixVols(:,3) = cubicMatrixVols(:,2) - (1/2);

mountMat = reshape(mountain(:,3), 100, 100);
mountainVols = newtonCotes3D(mountMat, 100, 1/(100-1))

asymmMat = reshape(asymmetric(:,3), 100, 100);
asymmVols = newtonCotes3D(asymmMat, 100, 2/99)
asymmVols(:,3) = asymmVols(:,2) - 1;

waveMat = reshape(wavelet(:,3), 100, 100);
waveVols = newtonCotes3D(waveMat, 100, 2/99)

gaussMat = reshape(gauss(:,3), 100, 100);
gaussVols = newtonCotes3D(gaussMat, 100, 20/99)
gaussVols(:,3) = gaussVols(:,2) - 1;

[X,Y] = meshgrid(0:1/99:1);
surf(X, Y, mountMat)
surf(X, Y, gaussMat)
surf(X, Y, waveMat)
surf(X, Y, asymmMat)