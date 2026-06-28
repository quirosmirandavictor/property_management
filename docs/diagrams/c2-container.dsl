workspace "Rent Manager - C2" "Container Diagram" {

    model {

        user = person "User" "System administrator or end user."

        dms = softwareSystem "Document Management System" "Manages users, documents, contracts, and photographs." {

            api = container "REST API" "Provides REST endpoints for authentication, user management, document management, contract management, and photograph management." "Python, FastAPI" {
                tags "API"
            }

            database = container "Database" "Stores users, roles, permissions, documents, contracts, metadata, and audit information." "MySQL" {
                tags "Database"
            }

            storage = container "File Storage" "Stores photographs and contract files." "Azure Blob Storage" {
                tags "Storage"
            }

        }

        user -> api "Uses" "HTTPS/JSON"

        api -> database "Reads and writes application data" "SQL"

        api -> storage "Uploads and downloads photographs and contract files" "HTTPS REST"

    }

    views {

        container dms {

            include *

            autolayout lr

            title "C2 - Document Management System"

        }

        theme default

        styles {

            element "Person" {
                background #08427b
                color #ffffff
                shape person
            }

            element "API" {
                background #438dd5
                color #ffffff
            }

            element "Database" {
                background #2e7d32
                color #ffffff
                shape cylinder
            }

            element "Storage" {
                background #8e44ad
                color #ffffff
            }

        }

    }

}