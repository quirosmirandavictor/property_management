workspace {

    model {

        admin = person "Administrator"

        tenant = person "Tenant"

        rentManager = softwareSystem "RentManager"

        mysql = softwareSystem "Azure Database for MySQL"

        admin -> rentManager "Uses"

        tenant -> rentManager "Uses"

        rentManager -> mysql "Reads/Writes"

    }

    views {

        systemContext rentManager {

            include *

            autoLayout lr

        }

        styles {

            element "Person" {
                shape Person
                background #0078D4
                color #ffffff
            }

            element "Software System" {
                background #0078D4
                color #ffffff
            }

            relationship "Relationship" {
                color #0078D4
                thickness 3
            }

        }

    }

}