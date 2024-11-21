#include <string>
#include <SDL_image.h>
#include <cmath>

using namespace std;

SDL_Surface* loadImage(string name){

    string path = "/Users/princemaphupha/Desktop/Games/HoleInOne/public/";
    string location = path + name;

    return IMG_Load(location.c_str());
}

float pythag(float x, float y){

    float result = 0.00;

    result = sqrt((pow(x, 2)) + pow(y, 2));

    return result;

}

float rectX(float baseX, float r, float ang){

    float x = 0;

    x = ((r / 2) * cos(ang)) + baseX;

    return x;

}

float rectY(float baseY, float r, float ang){

    float y = 0;

    y = ((r / 2) * cos(ang)) + baseY;

    return y;

}


