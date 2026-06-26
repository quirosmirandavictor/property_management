workspace "Rent Manager System - C3 IAM" "IAM Component Diagram" {

    model {

        user = person "User" "System administrator or end user."

        dms = softwareSystem "Rent Manager System" {

            api = container "REST API" "RESTful backend." "Python, FastAPI" {

                authController = component "Authentication Controller" {
                    description "Handles authentication requests."
                    technology "FastAPI Router"
                }

                userController = component "User Controller" {
                    description "Handles user and role management requests."
                    technology "FastAPI Router"
                }

                authService = component "Authentication Application Service" {
                    description "Executes the AuthenticateUser use case."
                    technology "Application Service"
                }

                userService = component "User Application Service" {
                    description "Executes CreateUser, ListUsers, AssignRole and GetUserFunctionalities use cases."
                    technology "Application Service"
                }

                jwtService = component "JWT Service" {
                    description "Generates and validates RS256 JWT tokens."
                    technology "PyJWT"
                }

                passwordHasher = component "Password Hasher" {
                    description "Hashes and verifies user passwords."
                    technology "Passlib / bcrypt"
                }

                userRepository = component "User Repository" {
                    description "Provides access to user and role persistence."
                    technology "Repository"
                }
            }

            database = container "Database" "Stores users, roles and permissions." "PostgreSQL"
        }

        user -> authController "Authenticates"

        user -> userController "Manages users"

        authController -> authService "Invokes"

        userController -> userService "Invokes"

        authService -> jwtService "Generates and validates tokens"

        authService -> passwordHasher "Verifies password"

        authService -> userRepository "Loads user"

        userService -> userRepository "Reads/Writes users and roles"

        userRepository -> database "Reads/Writes" "SQL"

    }

    views {

        component api {

            include *

            autolayout lr

            title "C3 - IAM Components"

        }

        theme default

    }

}