import { LineItem } from './line-item'
import { Statement } from './statement'

export interface InvoiceList {
  consInvNumber?: string
  invoiceNumber: string
  invoices: Invoice[],
  paymentMethod: string
  paymentSystem: string
  statusCode: string
  invoiceAmount: number
  paidAmount: number
}

export interface Invoice {
  bcolAccount: string
  businessIdentifier: string
  corpTypeCode: string
  createdBy: string
  createdName: string
  createdOn: string
  id: number
  lineItems: LineItem[]
  paid: number
  paymentMethod: string
  refund: number
  serviceFees: number
  statusCode: string
  total: number
  isOnlineBankingAllowed?: boolean
  paymentDate?: string
  refundDate?: string
}

export interface InvoiceListResponse {
  items: InvoiceList[]
  limit: number
  page: number
  total: number
}

export interface FailedInvoice {
  nsfCount?: number
  nsfFee?:number
  totalTransactionAmount?: number
  totalAmountToPay?: number
  invoices?: InvoiceList[]
  statements?: Statement[]
  reason?: string
}

export interface NonSufficientFundsInvoiceListResponse {
  invoices: InvoiceList[]
  statements: Statement[]
  total: number
  totalAmount: number
  totalAmountRemaining: number
  nsfAmount: number
  reason?: string
}
