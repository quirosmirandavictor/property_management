# Initial Data Model Proposal

This proposal keeps transactional and relational data in MySQL and stores binary files in Azure Blob Storage. MySQL tables only persist file metadata and Blob references.

## IAM

- `iam_users`: identity, contact data, credentials, activation status.
- `iam_roles`: role catalog.
- `iam_functionalities`: capability catalog exposed by the platform.
- `iam_user_roles`: many-to-many assignment between users and roles.
- `iam_role_functionalities`: many-to-many assignment between roles and functionalities.

Suggested core fields:

- `iam_users`: `id`, `dni`, `username`, `first_name`, `last_name`, `email`, `phone`, `password_hash`, `is_active`, `created_at`, `updated_at`.
- `iam_roles`: `id`, `name`, `description`.
- `iam_functionalities`: `id`, `code`, `name`, `description`.

## Assets

- `assets`: rentable properties or units.

Suggested core fields:

- `assets`: `id`, `asset_code`, `asset_type`, `name`, `address_line`, `bedroom_count`, `rental_value`, `balance_favor`, `status`, `created_at`, `updated_at`.

## Contracts

- `contracts`: lease agreement header.
- `tenant_contracts`: link between tenant users and contracts.
- `contract_documents`: metadata for contract files stored in Blob Storage.

Suggested core fields:

- `contracts`: `id`, `asset_id`, `start_date`, `end_date`, `rent_amount`, `deposit_amount`, `status`, `created_at`, `updated_at`.
- `tenant_contracts`: `id`, `contract_id`, `user_id`, `role_in_contract`.
- `contract_documents`: `id`, `contract_id`, `category`, `original_filename`, `content_type`, `size_bytes`, `blob_container`, `blob_key`, `uploaded_at`.

## Finance

- `expense_types`: catalog of expenses.
- `income_types`: catalog of incomes.
- `tax_types`: catalog of taxes.
- `payments`: payment records.
- `expenses`: expense records associated with assets.
- `incomes`: income records associated with assets.
- `invoices`: invoice header.
- `invoice_lines`: invoice detail lines.
- `payment_attachments`: metadata for payment evidence files stored in Blob Storage.
- `invoice_documents`: metadata for invoice documents stored in Blob Storage.

Suggested core fields:

- `payments`: `id`, `asset_id`, `registered_at`, `bank_reference`, `amount`, `description`, `status`.
- `expenses`: `id`, `asset_id`, `expense_type_id`, `payment_id`, `registered_at`, `amount`, `description`, `deductible`.
- `incomes`: `id`, `asset_id`, `income_type_id`, `payment_id`, `registered_at`, `amount`, `description`.
- `invoices`: `id`, `asset_id`, `issued_at`, `total_amount`, `status`.
- `invoice_lines`: `id`, `invoice_id`, `expense_id`, `income_id`, `line_type`, `amount`.

## Shared File Metadata Pattern

For any module that stores files in Blob Storage, keep a consistent reference structure in MySQL:

- `original_filename`
- `content_type`
- `size_bytes`
- `blob_container`
- `blob_key`
- `uploaded_at`

This keeps binary objects out of MySQL while preserving traceability, auditing, and application-level ownership.