#include <cmath>

class GolfBall {

    private:
        int x;
        int y;
        int w;
        int h;
        float vX;
        float vY;

    public:

        float getVelocity(){
            return sqrt(pow(vX, 2) + pow(vY, 2));
        }

        float getX(){
            return x;
        }

        float getY(){
            return y;
        }

        float getW(){
            return w;
        }

        float getH(){
            return h;
        }

        float getVX(){
            return vX;
        }

        float getVY(){
            return vY;
        }

        float setX(float xVal){
            x = xVal;
        }

        float setY(float yVal){
            y = yVal;
        }

        float setW(float wVal){
            w = wVal;
        }

        float setH(float hVal){
            h = hVal;
        }

        void setVX(float velX){
            vX = velX;
        }

        void setVY(float velY){
            vY = velY;
        }

};