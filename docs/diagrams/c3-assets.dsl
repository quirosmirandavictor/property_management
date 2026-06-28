workspace "Rent Manager System - C3 Assets" "Assets Component Diagram" {

    model {
        user = person "User" "System administrator or end user."

        dms = softwareSystem "Rent Manager System" {

            api = container "REST API" "RESTful backend." "Python, FastAPI" {

                assetController = component "Asset Controller" {
                    description "Handles REST requests for rentable property and unit management."
                    technology "FastAPI Router"
                }

                assetService = component "Asset Application Service" {
                    description "Executes CreateAsset, UpdateAsset, ListAssets and GetAsset use cases over the asset aggregate root."
                    technology "Application Service"
                }

                assetsPublicInterface = component "Assets Public Interface" {
                    description "Exposes get_asset_summary(asset_id), returning the asset data required by contracts and finance."
                    technology "Facade / Public Interface"
                }

                assetRepository = component "Asset Repository" {
                    description "Provides access to asset persistence in MySQL."
                    technology "Repository"
                }
            }

            contractsModule = container "Contracts Module" "Manages rental contracts." "Python, FastAPI" {
                contractService = component "Contract Application Service" {
                    description "Executes CreateContract; requires asset data when creating a contract."
                    technology "Application Service"
                }
            }

            financeModule = container "Finance Module" "Manages payments, expenses and income." "Python, FastAPI" {
                financeService = component "Finance Application Service" {
                    description "Registers AssetPayment, AssetExpense and AssetIncome; requires asset data."
                    technology "Application Service"
                }
            }

            database = container "Database" "Stores assets and their cross-module identifiers." "MySQL"
        }

        user -> assetController "Manages assets"
        assetController -> assetService "Invokes"
        assetService -> assetRepository "Reads/Writes assets"
        assetsPublicInterface -> assetService "Invokes (GetAsset)"
        contractService -> assetsPublicInterface "Gets asset summary (get_asset_summary) when creating a contract"
        financeService -> assetsPublicInterface "Gets asset summary (get_asset_summary) when registering payments, expenses and income"
        assetRepository -> database "Reads/Writes" "SQL"
    }

    views {
        component api {
            include *
            autolayout lr
            title "C3 - Assets Components"
        }
        theme default
    }
}
