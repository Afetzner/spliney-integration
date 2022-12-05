function coeff13 = coefficients(entries)
    row13 = ones(1, entries);
    row13(3:2:entries-2) = 2;
    row13(2:2:entries-1) = 4;
    coeff13 = ones(entries,entries);
    coeff13(1,:) = row13;
    coeff13(:,1) = row13';
    coeff13(:,entries) = row13;
    coeff13(entries,:) = row13';
    for x = 2:entries-1
        for y = 2:entries-1
            coeff13(x,y) = row13(x) * row13(y);
        end
    end
end