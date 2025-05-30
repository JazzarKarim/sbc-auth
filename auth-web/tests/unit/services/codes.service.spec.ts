import { Code } from '@/models/Code'
import CodesService from '../../../src/services/codes.service'

const testCodeSuspensionReasons = vi.hoisted(() => ({
  data: [{
    code: 'testSuspensionCode',
    desc: 'testSuspensionDesc',
    default: true
  }] as Code[]
}))

const mockob = {
  'PAY_API_URL': 'https://pay-api-dev.apps.silver.devops.gov.bc.ca/api/v1',
  'AUTH_API_URL': 'https://auth-api-dev.apps.silver.devops.gov.bc.ca/api/v1'
}

const mocks = vi.hoisted(() => ({
  get: vi.fn().mockReturnValue(testCodeSuspensionReasons)
}))

describe('Codes service', () => {
  beforeEach(() => {
    sessionStorage['AUTH_API_CONFIG'] = JSON.stringify(mockob)
    vi.doMock('axios', () => {
      return {
        get: mocks.get,
        interceptors: {
          request: {
            use: vi.fn(),
            eject: vi.fn()
          },
          response: {
            use: vi.fn(),
            eject: vi.fn()
          }
        }
      }
    })
  })

  it('call getCodes() for suspended_reason_codes ', () => {
    CodesService.getCodes('suspension-reason-codes').then((response) => {
      expect(response).toEqual(testCodeSuspensionReasons.data)
    })
  })
})
