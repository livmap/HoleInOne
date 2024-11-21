#include <iostream>
#include <SDL.h>
#include <SDL_image.h>
#include "utilities.h"
#include "golfball.h"

const float maxAxis = 32767.00;
const float aimMultiplier = 125.00;
const float friction = 1.00;

int main(int argc, char* argv[]) {

    // Initialize SDL with GameController support
    if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_GAMECONTROLLER) != 0) {
        std::cerr << "SDL_Init Error: " << SDL_GetError() << std::endl;
        return 1;
    }

    SDL_GameController* controller = nullptr;

    // Check for connected controllers
    if (SDL_NumJoysticks() > 0) {
        controller = SDL_GameControllerOpen(0);
        if (!controller) {
            std::cerr << "Could not open game controller! Error: " << SDL_GetError() << std::endl;
            SDL_Quit();
            return 1;
        }
        std::cout << "Game Controller connected: " << SDL_GameControllerName(controller) << std::endl;

        if (SDL_IsGameController(0)) {
            const char* mapping = SDL_GameControllerMapping(controller);
            std::cout << "Controller Mapping: " << mapping << std::endl;
        }
    }

    int WINDOW_WIDTH = 1000;
    int WINDOW_HEIGHT = 700;

    // Create SDL window and renderer
    SDL_Window* window = SDL_CreateWindow("SDL2 Joystick Block Movement",
                                          SDL_WINDOWPOS_CENTERED,
                                          SDL_WINDOWPOS_CENTERED,
                                          WINDOW_WIDTH, WINDOW_HEIGHT,
                                          SDL_WINDOW_SHOWN);
    if (!window) {
        std::cerr << "Window could not be created! Error: " << SDL_GetError() << std::endl;
        if (controller) SDL_GameControllerClose(controller);
        SDL_Quit();
        return 1;
    }

    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (!renderer) {
        std::cerr << "Renderer could not be created! Error: " << SDL_GetError() << std::endl;
        SDL_DestroyWindow(window);
        if (controller) SDL_GameControllerClose(controller);
        SDL_Quit();
        return 1;
    }

    SDL_Surface* bgSurface = loadImage("background.jpg");
    SDL_Texture* bgTexture = SDL_CreateTextureFromSurface(renderer, bgSurface);
    SDL_FreeSurface(bgSurface);

    // Golf Ball
    GolfBall ball;
    ball.setX(500);
    ball.setY(350);
    ball.setW(20);
    ball.setH(20);

    SDL_Surface* imageSurface = loadImage("golfball.png");
    SDL_Texture* imageTexture = SDL_CreateTextureFromSurface(renderer, imageSurface);
    SDL_FreeSurface(imageSurface);

    SDL_Rect destRect = {ball.getX(), ball.getY(), ball.getW(), ball.getH()};

    SDL_Surface* compassSurface = loadImage("compass.png");
    SDL_Texture* compassTexture = SDL_CreateTextureFromSurface(renderer, compassSurface);
    SDL_FreeSurface(compassSurface);

    SDL_Rect compassRect = {ball.getX(), ball.getY(), 50, 50};

    SDL_Surface* holeSurface = loadImage("hole.png");
    SDL_Texture* holeTexture = SDL_CreateTextureFromSurface(renderer, holeSurface);
    SDL_FreeSurface(holeSurface);

    SDL_Rect holeRect = {800, 350, 25, 25};


    // Line
    SDL_Point lineStart = {ball.getX() + (ball.getW() / 2), ball.getY() + (ball.getH() / 2)};
    float lineWidth = 0;

    float maxX = 0;
    float maxY = 0;
    float deadzone = 3000;

    int lineR = 0;
    int lineG = 255;
    int lineB = 0;

    bool hitPhase = false;

    // Game loop
    bool running = true;
    SDL_Event event;

    float angle = 150.0f;

    while (running) {
        // Event polling
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running = false;
            }

            if (event.type == SDL_CONTROLLERBUTTONDOWN) {
                if (event.cbutton.button == SDL_CONTROLLER_BUTTON_A) {
                    std::cout << "A button pressed!" << std::endl;



                }
            }

            if (event.type == SDL_CONTROLLERBUTTONUP) {
                if (event.cbutton.button == SDL_CONTROLLER_BUTTON_A) {
                    std::cout << "A button released!" << std::endl;
                }
            }
        }

        /*

        if (SDL_GameControllerGetButton(controller, SDL_CONTROLLER_BUTTON_A)) {
            std::cout << "A button pressed!" << std::endl;

            hitPhase = true;
        }

        */

        // Read joystick input
        int xAxis = SDL_GameControllerGetAxis(controller, SDL_CONTROLLER_AXIS_LEFTX);
        int yAxis = SDL_GameControllerGetAxis(controller, SDL_CONTROLLER_AXIS_LEFTY);

        if(xAxis > deadzone || xAxis < -deadzone){
            if(xAxis < 0){
                lineWidth = 125 * (-pythag(xAxis, yAxis) / maxAxis);
            } else {
                lineWidth = 125 * (pythag(xAxis, yAxis) / maxAxis);
            }

        } else{
            lineWidth = 0;
        }


        float diff = (pythag(xAxis, yAxis) / pythag(maxAxis, maxAxis)) * 255.00;
        lineR = diff;
        lineG = 255.00 - diff;

        angle = atan((yAxis * 1.00) / (xAxis * 1.00));

        // Normalize axis values and apply deadzone

        SDL_Point lineEnd;
        lineEnd.x = ball.getX() + (lineWidth * cos(angle));
        lineEnd.y = ball.getY() + (lineWidth * sin(angle));

        SDL_RenderClear(renderer);

        SDL_RenderCopy(renderer, bgTexture, NULL, NULL);
        SDL_SetRenderDrawColor(renderer, lineR, lineG, lineB, 255);
        SDL_RenderDrawLine(renderer, lineStart.x, lineStart.y, lineEnd.x, lineEnd.y);
        SDL_RenderCopy(renderer, imageTexture, NULL, &destRect);
        SDL_RenderCopy(renderer, holeTexture, NULL, &holeRect);

        SDL_RenderPresent(renderer);
    }

    // Clean up
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    if (controller) SDL_GameControllerClose(controller);
    SDL_Quit();

    return 0;
}
