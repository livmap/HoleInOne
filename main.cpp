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

    // Check for connected controllers
    if (SDL_NumJoysticks() > 0) {
        // Try to open the first available game controller
        SDL_GameController* controller = SDL_GameControllerOpen(0);
        if (!controller) {
            std::cerr << "Could not open game controller! Error: " << SDL_GetError() << std::endl;
            SDL_Quit();
            return 1;
        }
        std::cout << "Game Controller connected: " << SDL_GameControllerName(controller) << std::endl;

    if (SDL_IsGameController(0)) {
    SDL_GameController* controller = SDL_GameControllerOpen(0);
    if (controller) {
        const char* mapping = SDL_GameControllerMapping(controller);
        std::cout << "Controller Mapping: " << mapping << std::endl;
        SDL_GameControllerClose(controller);
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
        SDL_GameControllerClose(controller);
        SDL_Quit();
        return 1;
    }

    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (!renderer) {
        std::cerr << "Renderer could not be created! Error: " << SDL_GetError() << std::endl;
        SDL_DestroyWindow(window);
        SDL_GameControllerClose(controller);
        SDL_Quit();
        return 1;
    }

    SDL_Surface* bgSurface = loadImage("background.jpg");
    SDL_Texture* bgTexture = SDL_CreateTextureFromSurface(renderer, bgSurface);
    SDL_FreeSurface(bgSurface); 


    // Golf Ball

    GolfBall ball;
    ball.x = 500;
    ball.y = 350;
    ball.w = 20;
    ball.h = 20;

    SDL_Surface* imageSurface = loadImage("golfball.png");
    SDL_Texture* imageTexture = SDL_CreateTextureFromSurface(renderer, imageSurface);
    SDL_FreeSurface(imageSurface);

    SDL_Rect destRect;
    destRect.x = ball.x;
    destRect.y = ball.y;
    destRect.w = ball.w;
    destRect.h = ball.h;

    SDL_Surface* compassSurface = loadImage("compass.png");
    SDL_Texture* compassTexture = SDL_CreateTextureFromSurface(renderer, compassSurface);
    SDL_FreeSurface(compassSurface);

    SDL_Rect compassRect;
    compassRect.x = ball.x;
    compassRect.y = ball.y;
    compassRect.w = 50;
    compassRect.h = 50;

    SDL_Surface* holeSurface = loadImage("hole.png");
    SDL_Texture* holeTexture = SDL_CreateTextureFromSurface(renderer, holeSurface);
    SDL_FreeSurface(holeSurface);

    SDL_Rect holeRect;
    holeRect.x = 800;
    holeRect.y = 350;
    holeRect.w = 25;
    holeRect.h = 25;

    SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255);
    SDL_Rect rect = { ball.x + (ball.w / 2), ball.y + (ball.h / 2), 0, 0 };

    SDL_Point center;
    center.x = rect.w / 2;
    center.y = rect.y / 2;

    // Line
    SDL_Point lineStart;
    lineStart.x = ball.x + (ball.w / 2);
    lineStart.y = ball.y + (ball.h / 2);

    


    float maxX = 0;
    float maxY = 0;
    float deadzone = 3000;

    int lineR = 0;
    int lineG = 255;
    int lineB = 0;

    bool hitPhase = 1;

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
        }

        if (event.type == SDL_CONTROLLERBUTTONDOWN) {
            if (event.cbutton.button == SDL_CONTROLLER_BUTTON_A) {
                std::cout << "A button pressed!" << std::endl;
                
            }
        }

        if (event.type == SDL_CONTROLLERBUTTONUP) {
            if (event.cbutton.button == SDL_CONTROLLER_BUTTON_A) {
                std::cout << "A button released!" << std::endl;
                // Add your A button release functionality here
            }
        }

        if (SDL_GameControllerGetButton(controller, SDL_CONTROLLER_BUTTON_A)) {
            std::cout << "A button pressed!" << std::endl;
            hitPhase = 1;
        }

        

        // Read joystick input
            // Read axis values (axes typically range from -32768 to 32767)
        int xAxis = SDL_GameControllerGetAxis(controller, SDL_CONTROLLER_AXIS_LEFTX);
        int yAxis = SDL_GameControllerGetAxis(controller, SDL_CONTROLLER_AXIS_LEFTY);  
        int rightX = SDL_GameControllerGetAxis(controller, SDL_CONTROLLER_AXIS_RIGHTX); 
        int rightY = SDL_GameControllerGetAxis(controller, SDL_CONTROLLER_AXIS_RIGHTY);        


        
        if(xAxis > deadzone || xAxis < -deadzone){
            if(xAxis < 0){
                rect.w = 125 * (-pythag(xAxis, yAxis) / maxAxis);
            } else {
                rect.w = 125 * (pythag(xAxis, yAxis) / maxAxis);
            }
            
        } else{
            rect.w = 0;
        }


        float diff = (pythag(xAxis, yAxis) / pythag(maxAxis, maxAxis)) * 255.00;
        lineR = diff;
        lineG = 255.00 - diff;

        angle = atan((yAxis * 1.00) / (xAxis * 1.00));

        
        

        // Normalize axis values and apply deadzone

        SDL_Point lineEnd;
        lineEnd.x = ball.x + (rect.w * cos(angle));
        lineEnd.y = ball.y + (rect.w * sin(angle));

        
        

        SDL_RenderClear(renderer);

        SDL_RenderCopy(renderer, bgTexture, NULL, NULL);
        SDL_SetRenderDrawColor(renderer, lineR, lineG, lineB, 255);
        SDL_RenderDrawLine(renderer, lineStart.x, lineStart.y, lineEnd.x, lineEnd.y);
        //SDL_RenderFillRect(renderer, &rect);
        //SDL_RenderCopyEx(renderer, nullptr, nullptr, &rect, angle, &center, SDL_FLIP_NONE);
        SDL_RenderCopy(renderer, imageTexture, NULL, &destRect);
        SDL_RenderCopy(renderer, holeTexture, NULL, &holeRect);
        

        SDL_RenderPresent(renderer);
    }

    // Clean up
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_GameControllerClose(controller);
    SDL_Quit();

    return 0;
}
}