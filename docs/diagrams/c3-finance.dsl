workspace "Rent Manager System - C3 Finance" "Finance Component Diagram" {

    model {

        user = person "User" "System administrator or end user." {
            tags "Person"
        }

        rms = softwareSystem "Rent Manager System" {

            api = container "REST API" "RESTful backend." "Python, FastAPI" {
                tags "API"

                financeController = component "Finance Controller" {
                    description "Handles REST requests for payments, expenses, incomes and invoices."
                    technology "FastAPI Router"
                    tags "Controller"
                }

                financeService = component "Finance Application Service" {
                    description "Executes RegisterPayment, RegisterExpense, RegisterIncome, CreateInvoice and ListFinanceRecords use cases."
                    technology "Application Service"
                    tags "Service"
                }

                financePublicInterface = component "Finance Public Interface" {
                    description "Exposes get_finance_summary(asset_id) for cross-module reporting and validations."
                    technology "Facade / Public Interface"
                    tags "PublicInterface"
                }

                paymentRepository = component "Payment Repository" {
                    description "Provides access to payment persistence and evidence metadata."
                    technology "Repository"
                    tags "Repository"
                }

                expenseRepository = component "Expense Repository" {
                    description "Provides access to expense persistence and expense-type catalog queries."
                    technology "Repository"
                    tags "Repository"
                }

                incomeRepository = component "Income Repository" {
                    description "Provides access to income persistence and income-type catalog queries."
                    technology "Repository"
                    tags "Repository"
                }

                invoiceRepository = component "Invoice Repository" {
                    description "Provides access to invoice aggregates, lines and invoice document metadata."
                    technology "Repository"
                    tags "Repository"
                }
            }

            assetsModule = container "Assets Module" "Provides asset data." "Python, FastAPI" {
                assetsPublicInterface = component "Assets Public Interface" {
                    description "Exposes get_asset_summary(asset_id) for finance validations."
                    technology "Facade / Public Interface"
                    tags "ModuleAPI"
                }
            }

            contractsModule = container "Contracts Module" "Provides contract data." "Python, FastAPI" {
                contractsPublicInterface = component "Contracts Public Interface" {
                    description "Exposes get_contract_summary(contract_id) for invoice and payment validations."
                    technology "Facade / Public Interface"
                    tags "ModuleAPI"
                }
            }

            database = container "Database" "Stores payments, expenses, incomes, invoices and related metadata." "MySQL" {
                tags "Database"
            }
        }

        user -> financeController "Manages finance records"
        financeController -> financeService "Invokes"
        financeService -> assetsPublicInterface "Gets asset summary before registering records"
        financeService -> contractsPublicInterface "Gets contract summary when issuing invoices"
        financeService -> paymentRepository "Reads/Writes payments"
        financeService -> expenseRepository "Reads/Writes expenses"
        financeService -> incomeRepository "Reads/Writes incomes"
        financeService -> invoiceRepository "Reads/Writes invoices"
        financePublicInterface -> financeService "Invokes (GetFinanceSummary)"
        paymentRepository -> database "Reads/Writes" "SQL"
        expenseRepository -> database "Reads/Writes" "SQL"
        incomeRepository -> database "Reads/Writes" "SQL"
        invoiceRepository -> database "Reads/Writes" "SQL"

    }

    views {

        component api {

            include *

            autolayout lr

            title "C3 - Finance Components"

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
