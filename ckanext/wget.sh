#!/usr/bin/env bash
echo 'Downloading images'
wget --no-check-certificate https://datanouvelleaquitaine.org/wp-content/uploads/2019/03/administration.png
wget --no-check-certificate https://datanouvelleaquitaine.org/wp-content/uploads/2019/03/agriculture.png
wget --no-check-certificate https://datanouvelleaquitaine.org/wp-content/uploads/2019/03/amenagement.png
wget --no-check-certificate https://datanouvelleaquitaine.org/wp-content/uploads/2019/03/citoyennete.png
wget --no-check-certificate https://datanouvelleaquitaine.org/wp-content/uploads/2019/03/culture.png
wget --no-check-certificate https://datanouvelleaquitaine.org/wp-content/uploads/2019/03/economie.png
wget --no-check-certificate https://datanouvelleaquitaine.org/wp-content/uploads/2019/03/energie.png
wget --no-check-certificate https://datanouvelleaquitaine.org/wp-content/uploads/2019/03/environnement.png
wget --no-check-certificate https://datanouvelleaquitaine.org/wp-content/uploads/2019/03/equipement.png
wget --no-check-certificate https://datanouvelleaquitaine.org/wp-content/uploads/2019/03/formation.png
wget --no-check-certificate https://datanouvelleaquitaine.org/wp-content/uploads/2019/03/imagerie.png
wget --no-check-certificate https://datanouvelleaquitaine.org/wp-content/uploads/2019/03/limites-administratives.png
wget --no-check-certificate https://datanouvelleaquitaine.org/wp-content/uploads/2019/03/mer.png
wget --no-check-certificate https://datanouvelleaquitaine.org/wp-content/uploads/2019/03/mobilite.png
wget --no-check-certificate https://datanouvelleaquitaine.org/wp-content/uploads/2019/03/sciences.png
wget --no-check-certificate https://datanouvelleaquitaine.org/wp-content/uploads/2019/03/sante.png
echo 'Cropping images'
mogrify -crop 60x60+0+0 *.png
