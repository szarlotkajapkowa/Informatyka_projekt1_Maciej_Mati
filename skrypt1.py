# -*- coding: utf-8 -*-
"""
Created on Tue May  7 21:45:59 2024

@author: mateu
"""

import sys
import math
import argparse
import csv
import numpy as np

class CoordinateTransformer:
    def __init__(self):
        # Stałe dla elipsoid
        self.elipsoidy = {
            'GRS80': {'a': 6378137.0, 'e2': 0.00669438002290},
            'WGS84': {'a': 6378137.0, 'e2': 0.00669437999014},
            'Krasowski': {'a': 6378245.0, 'e2': 0.00669342162297}
        }

    def wpisz_elipsoide(self, nazwa):
        if nazwa not in self.elipsoidy:
            raise ValueError(f'nie ma takiej elipsoidy: {nazwa}')
        return self.elipsoidy[nazwa]['a'], self.elipsoidy[nazwa]['e2']

def XYZ_do_BLH(self, x, y, z, a, e2):
    p = math.sqrt(x**2 + y**2)
    theta = math.atan2(z * a, p * (1 - e2))
    lon = math.atan2(y, x)
    lat = math.atan2(z + e2 * a * math.sin(theta)**3, p - e2 * a * math.cos(theta)**3)
    N = a / math.sqrt(1 - e2 * math.sin(lat)**2)
    h = p / math.cos(lat) - N
    lat_deg = math.degrees(lat)
    lon_deg = math.degrees(lon)
    return lat_deg, lon_deg, h

    """Ta funkcja zamienia współrzędne XYZ na współrzędne geodezyjne"""
    def BLH_do_XYZ(self, lat, lon, h, a, e2):
        lat_rad = math.radians(lat)
        lon_rad = math.radians(lon)
        N = a / math.sqrt(1 - e2 * math.sin(lat_rad)**2)
        x = (N + h) * math.cos(lat_rad) * math.cos(lon_rad)
        y = (N + h) * math.cos(lat_rad) * math.sin(lon_rad)
        z = (N * (1 - e2) + h) * math.sin(lat_rad)
        return x, y, z
    """Ta funkcja zamienia współrzędne geodezyjne(BLH) na XYZ."""
    

    def XYZ_do_NEU(self, x, y, z, lat, lon):
        lat_rad = math.radians(lat)
        lon_rad = math.radians(lon)
        R = self.rneu(lat_rad, lon_rad)
        dxyz = np.array([x, y, z])
        R = np.array(R)
        neup = R @ dxyz
        return neup[0], neup[1], neup[2]
    """Ta funkcja przekrztałca współrzędne XYZ do NEU"""



    def rneu(self, lat, lon):
        return np.array([[-math.sin(lat) * math.cos(lon), -math.sin(lat) * math.sin(lon), math.cos(lat)],
                [-math.sin(lon), math.cos(lon), 0],
                [math.cos(lat) * math.cos(lon), math.cos(lat) * math.sin(lon), math.sin(lat)]])

    def fl2gk(self, lat, lon, lon0, a, e2):
        b2 = a * (1 - e2)
        e2p = (a**2 - b2) / b2
        dlon = lon - lon0
        t = math.tan(math.radians(lat))
        ni = math.sqrt(e2p * (math.cos(math.radians(lat)))**2)
        N = a / math.sqrt(1 - e2 * math.sin(math.radians(lat))**2)
        sigma = self.sigma(math.radians(lat), a, e2)

        xgk = sigma + ((math.radians(dlon)**2) / 2) * N * math.sin(math.radians(lat)) * math.cos(math.radians(lat)) * \
              (1 + ((math.radians(dlon)**2) / 12) * (math.cos(math.radians(lat)))**2 * \
              (5 - t**2 + 9 * ni**2 + 4 * ni**4) + \
              ((math.radians(dlon)**4) / 360) * (math.cos(math.radians(lat))**4) * \
              (61 - 58 * t**2 + t**4 + 270 * ni**2 - 330 * ni**2 * t**2))

        ygk = (math.radians(dlon) * N * math.cos(math.radians(lat))) * \
              (1 + (((math.radians(dlon))**2 / 6) * (math.cos(math.radians(lat)))**2) * \
              (1 - t**2 + ni**2) + ((math.radians(dlon)**4) / 120) * (math.cos(math.radians(lat))**4) * \
              (5 - 18 * t**2 + t**4 + 14 * ni**2 - 58 * ni**2 * t**2))

        return xgk, ygk


    """Ta funkcja zamienia współrzędne geodezyjne(FL) na współrzędne Gaussa-Krugera."""


    def sigma(self, lat, a, e2):
        A0 = 1 - e2 / 4 - 3 * e2**2 / 64 - 5 * e2**3 / 256
        A2 = (3 / 8) * (e2 + e2**2 / 4 + 15 * e2**3 / 128)
        A4 = (15 / 256) * (e2**2 + 3 * e2**3 / 4)
        A6 = 35 * e2**3 / 3072
        sigma = a * (A0 * lat - A2 * math.sin(2 * lat) + A4 * math.sin(4 * lat) - A6 * math.sin(6 * lat))
        return sigma

    def BL_do_2000(self, lat, lon, elipsoida):
        a, e2 = self.wpisz_elipsoide(elipsoida)
        if lon < 13.5 or lon >= 25.5:
            raise ValueError(f'Lambda {lon} poza zasiegiem ukladu 2000')
        zone = int((lon + 1.5) // 3)
        lon0 = 15 + 3 * (zone - 5)
        xgk, ygk = self.fl2gk(lat, lon, lon0, a, e2)
        m2000 = 0.999923
        x2000 = xgk * m2000
        y2000 = ygk * m2000 + zone * 1000000 + 500000
        return x2000, y2000


    """Ta funkcja zamienia współrzędne geodezyjne(FL) na współrzędne w układzie 2000."""


    def BL_do_1992(self, lat, lon, elipsoida):
        a, e2 = self.wpisz_elipsoide(elipsoida)
        lon0 = 19
        xgk, ygk = self.fl2gk(lat, lon, lon0, a, e2)
        m1992 = 0.9993
        x1992 = xgk * m1992 - 5300000
        y1992 = ygk * m1992 + 500000
        return x1992, y1992

    """Ta funkcja zamienia współrzędne geodezyjne(FL) na współrzędne w układzie 1992."""


def parse_arguments():
    parser = argparse.ArgumentParser(description='transformacja zmiany wspolrzednych')
    parser.add_argument('--input', required=True, help='Wprowadz plik CSV ze wspolrzednymi')
    parser.add_argument('--output', required=True, help='Wyjściowy plik CSV dla przekształconych współrzędnych')
    parser.add_argument('--transformacja', required=True, choices=['XYZ_do_BLH', 'BLH_do_XYZ', 'XYZ_do_NEU', 'BL_do_2000', 'BL_do_1992'], help='Typ transformacji')
    parser.add_argument('--elipsoida', default='GRS80', help='Elipsoidy do uzycia do transformacji (GRS80, WGS84, Krasowski)')
    return parser.parse_args()

def main():
    args = parse_arguments()
    transformer = CoordinateTransformer()

    # Załaduj plik
    with open(args.input, newline='') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        data = [list(map(float, row)) for row in reader]

   
    results = []
    try:
        if args.transformacja == 'XYZ_do_BLH':
            a, e2 = transformer.wpisz_elipsoide(args.elipsoida)
            for x, y, z in data:
                lat, lon, h = transformer.XYZ_do_BLH(x, y, z, a, e2)
                results.append([lat, lon, h])
        elif args.transformacja == 'BLH_do_XYZ':
            a, e2 = transformer.wpisz_elipsoide(args.elipsoida)
            for lat, lon, h in data:
                x, y, z = transformer.BLH_do_XYZ(lat, lon, h, a, e2)
                results.append([x, y, z])
        elif args.transformacja == 'XYZ_do_NEU':
            lat, lon = data[0][:2]
            for x, y, z in data:
                n, e, u = transformer.XYZ_do_NEU(x, y, z, lat, lon)
                results.append([n, e, u])
        elif args.transformacja == 'BL_do_2000':
            for lat, lon in data:
                x2000, y2000 = transformer.BL_do_2000(lat, lon, args.elipsoida)
                results.append([x2000, y2000])
        elif args.transformacja == 'BL_do_1992':
            for lat, lon in data:
                x1992, y1992 = transformer.BL_do_1992(lat, lon, args.elipsoida)
                results.append([x1992, y1992])
    except ValueError as e:
        print(f'Error: {e}')
        sys.exit(1)

    # Zapisz wyniki aby wyswietlić plik
    with open(args.output, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Wyniki transformacji'])  
        writer.writerows(results)

if __name__ == "__main__":
    main()

