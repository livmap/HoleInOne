#include <SDL.h>
#include <iostream>
#include <cmath>

const int SCREEN_WIDTH = 800;
const int SCREEN_HEIGHT = 600;
const float ROTATION_SPEED = 90.0f; // Degrees per second

// Function to rotate a point around the center
SDL_Point rotatePoint(SDL_Point point, SDL_Point center, float angle) {
    float radians = angle * M_PI / 180.0f;
    float s = sin(radians);
    float c = cos(radians);

    // Translate point to origin
    point.x -= center.x;
    point.y -= center.y;

    // Rotate the point
    float newX = point.x * c - point.y * s;
    float newY = point.x * s + point.y * c;

    // Translate point back
    point.x = static_cast<int>(newX + center.x);
    point.y = static_cast<int>(newY + center.y);

    return point;
}

int main(int argc, char* argv[]) {
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        std::cerr << "SDL could not initialize! SDL_Error: " << SDL_GetError() << std::endl;
        return -1;
    }

    SDL_Window* window = SDL_CreateWindow("Filled Rotating Rectangle", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN);
    if (!window) {
        std::cerr << "Window could not be created! SDL_Error: " << SDL_GetError() << std::endl;
        SDL_Quit();
        return -1;
    }

    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (!renderer) {
        std::cerr << "Renderer could not be created! SDL_Error: " << SDL_GetError() << std::endl;
        SDL_DestroyWindow(window);
        SDL_Quit();
        return -1;
    }

    bool quit = false;
    SDL_Event e;

    float angle = 0.0f; // Rotation angle
    Uint32 lastTime = SDL_GetTicks();

    while (!quit) {
        while (SDL_PollEvent(&e) != 0) {
            if (e.type == SDL_QUIT) {
                quit = true;
            }
        }

        Uint32 currentTime = SDL_GetTicks();
        float deltaTime = (currentTime - lastTime) / 1000.0f;
        lastTime = currentTime;

        angle += ROTATION_SPEED * deltaTime;
        if (angle >= 360.0f) {
            angle -= 360.0f;
        }

        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        SDL_RenderClear(renderer);

        // Define rectangle dimensions and center
        int rectWidth = 200;
        int rectHeight = 10;
        SDL_Point center = {SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2};

        // Draw the filled rectangle line by line
        SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255);
        for (int yOffset = -rectHeight / 2; yOffset < rectHeight / 2; ++yOffset) {
            SDL_Point lineStart = {center.x - rectWidth / 2, center.y + yOffset};
            SDL_Point lineEnd = {center.x + rectWidth / 2, center.y + yOffset};

            // Rotate both endpoints of the line
            lineStart = rotatePoint(lineStart, center, angle);
            lineEnd = rotatePoint(lineEnd, center, angle);

            // Draw the line
            SDL_RenderDrawLine(renderer, lineStart.x, lineStart.y, lineEnd.x, lineEnd.y);
        }

        SDL_RenderPresent(renderer);
    }

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}
