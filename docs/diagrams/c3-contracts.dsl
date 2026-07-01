workspace "Rent Manager System - C3 Contracts" "Contracts Component Diagram" {

    model {

        user = person "User" "System administrator or end user." {
            tags "Person"
        }

        rms = softwareSystem "Rent Manager System" {

            api = container "REST API" "RESTful backend." "Python, FastAPI" {
                tags "API"

                contractController = component "Contract Controller" {
                    description "Handles REST requests for contract lifecycle operations."
                    technology "FastAPI Router"
                    tags "Controller"
                }

                contractService = component "Contract Application Service" {
                    description "Executes CreateContract, UpdateContract, ListContracts, AddContractTenant and AddContractDocument use cases."
                    technology "Application Service"
                    tags "Service"
                }

                contractsPublicInterface = component "Contracts Public Interface" {
                    description "Exposes get_contract_summary(contract_id), returning contract data required by other modules."
                    technology "Facade / Public Interface"
                    tags "PublicInterface"
                }

                contractRepository = component "Contract Repository" {
                    description "Provides access to contract aggregate persistence in MySQL."
                    technology "Repository"
                    tags "Repository"
                }
            }

            assetsModule = container "Assets Module" "Provides asset data." "Python, FastAPI" {
                assetsPublicInterface = component "Assets Public Interface" {
                    description "Exposes get_asset_summary(asset_id) for contract validations."
                    technology "Facade / Public Interface"
                    tags "ModuleAPI"
                }
            }

            iamModule = container "IAM Module" "Provides user and role data." "Python, FastAPI" {
                iamPublicInterface = component "IAM Public Interface" {
                    description "Exposes get_user_summary(user_id) for tenant validation in contracts."
                    technology "Facade / Public Interface"
                    tags "ModuleAPI"
                }
            }

            database = container "Database" "Stores contracts, tenant links and contract documents metadata." "MySQL" {
                tags "Database"
            }
        }

        user -> contractController "Manages contracts"
        contractController -> contractService "Invokes"
        contractService -> assetsPublicInterface "Gets asset summary before creating/updating contracts"
        contractService -> iamPublicInterface "Gets user summary before linking tenant contracts"
        contractService -> contractRepository "Reads/Writes contracts"
        contractsPublicInterface -> contractService "Invokes (GetContract)"
        contractRepository -> database "Reads/Writes" "SQL"

    }

    views {

        component api {

            include *

            autolayout lr

            title "C3 - Contracts Components"

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

            element "Controller" {
                background #0078D4
                color #ffffff
            }

            element "Service" {
                background #438dd5
                color #ffffff
            }

            element "PublicInterface" {
                background #8e44ad
                color #ffffff
            }

            element "Repository" {
                background #2e7d32
                color #ffffff
            }

            element "ModuleAPI" {
                background #08427b
                color #ffffff
            }

            element "Database" {
                background #2e7d32
                color #ffffff
                shape cylinder
            }

            relationship "Relationship" {
                color #0078D4
                thickness 2
            }

        }

    }

}
