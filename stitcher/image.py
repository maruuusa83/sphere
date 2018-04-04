# coding: utf-8

import cv2
import numpy

from clib import PyStitcher

class SphereImageGenerator:
    u'''SphereImageGenerator class

    全天球画像の生成を行うクラスです。
    '''

    def stitch(self, images):
        u'''result = stitch(images);
        画像へのパスのリストを与えると, 画像を結合して保存したパスを返却します。
        '''
        argstr = '';
        for image in images:
            if argstr == '':
                argstr = str(image);
            else:
                argstr = argstr + ' ' + str(image);
            
        PyStitcher.stitch(argstr);

    def imjoin(self, img1, img2):
        u'''result_img = imjoin(img1, img2)
        画像を二つ与えるとその二つを結合して返却します。
        AKAZE特徴量を用いた結合を行います。
        '''
        # 特徴点検出
        keypoints_img1 = self._getKeypoints(img1);
        keypoints_img2 = self._getKeypoints(img2);

        # 特徴量記述
        keypoints_img1, descripts_img1 = self._getDescripts(img1, keypoints_img1);
        keypoints_img2, descripts_img2 = self._getDescripts(img2, keypoints_img2);

        # マッチング
        matches = self._getMatches(descripts_img1, descripts_img2);

        out1 = cv2.drawKeypoints(img1, keypoints_img1, None, None, cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS);
        out2 = cv2.drawKeypoints(img2, keypoints_img2, None, None, cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS);

        matches = sorted(matches, key=lambda val: val.distance);

        # マッチングの厳選
        dist = [m.distance for m in matches];
        thres_dist = (sum(dist) / len(dist)) * 0.9;
        sel_matches = [m for m in matches if m.distance < thres_dist];

        # 変形情報の算出
        H, move = self._getDeformParams(keypoints_img1, keypoints_img2, sel_matches);

        # 実際の変形
        h_img1, w_img1 = img1.shape[:2];
        h_img2, w_img2 = img2.shape[:2];

        dst = cv2.warpPerspective(img2, H, (w_img2 + move[0], h_img2 + move[1]));
        for i in range(w_img1):
            for j in range(h_img1):
                dst[j, i] = img1[j, i];

        img_matchings = cv2.drawMatches(img1, keypoints_img1, img2, keypoints_img2, sel_matches, img1);

        return ([out1, out2, img_matchings, dst]);


    def _getKeypoints(self, img):
        u'''keypoints = _getKeypoints(img)
        画像を与えると特徴点のリストを返します。
        '''
        detector  = cv2.FeatureDetector_create("AKAZE");
        return (detector.detect(img));


    def _getDescripts(self, img, keypoints):
        u'''keypoints, descripts = _getDescripts(img, keypoints)
        画像と特徴点のリストを与えると、特徴量記述を返します。
        '''
        extractor = cv2.DescriptorExtractor_create("AKAZE");
        return (extractor.compute(img, keypoints));


    def _getMatches(self, descript1, descript2):
        u'''matches = _getMatches(descript1, descript2)
        特徴量記述の組を与えると, マッチングのリストを返します。
        '''
        matcher = cv2.DescriptorMatcher_create('BruteForce-Hamming');
        return (matcher.match(descript1, descript2));

    def _getDeformParams(self, keypoints1, keypoints2, matches):
        u'''H, move = _getDeformParams(keypoints1, keypoints2, matches)
        キーポイントセットとそのマッチング情報から変形に必要な情報を算出します。
        ホモグラフィ行列算出にはRANSACによるロバスト推定を行います。
        H: ホモグラフィ行列
        move: 画像の移動量[x, y]となる配列
        '''
        # ホモグラフィ行列の算出
        p1 = [[keypoints1[m.queryIdx].pt[0], keypoints1[m.queryIdx].pt[1]] for m in matches];
        p2 = [[keypoints2[m.trainIdx].pt[0], keypoints2[m.trainIdx].pt[1]] for m in matches];
        p1 = numpy.array(p1);
        p2 = numpy.array(p2);

        H, mask = cv2.findHomography(p2, p1, cv2.RANSAC);

        # 移動すべき量の算出
        x = y = cnt = 0;
        for i, v in enumerate(mask):
            if v == 1:
                x += p1[i][0] - p2[i][0];
                y += p1[i][1] - p2[i][1];
                cnt += 1;

        x = abs(int(round(x / cnt)));
        y = abs(int(round(y / cnt)));

        return (H, [x, y]);


