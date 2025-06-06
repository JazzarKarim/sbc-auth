<template>
  <v-container class="view-container">
    <div class="view-header flex-column mb-10">
      <h1 class="view-header__title">
        Getting your identity affidavit notarized
      </h1>
      <p class="mt-5 mb-3">
        Download the identity affidavit template below and visit a Notary Public or lawyer to have it notarized.
      </p>
    </div>
    <v-card
      flat
      class="pa-sm-6 pa-lg-8"
    >
      <p class="mb-8">
        <strong>You will need to bring:</strong>
      </p>
      <div class="mb-9">
        <ol>
          <li>One piece of government-issued photo identification</li>
          <li>
            Bring a printed copy of the BC Registries and Online Services affidavit template.
            You must use this template and fill out all fields.
            Failure to do so may result in a rejection of your account request.
          </li>
          <li>Payment (most notaries and lawyers charge a fee for this service. Fees will vary.)</li>
        </ol>
      </div>
      <p class="mb-10">
        Once you have your affidavit notarized, return to this website and continue to the next step.
        <span class="lb">You will upload your affidavit later in the account creation process.</span>
      </p>
      <div class="d-inline-flex flex-column pb-2">
        <v-btn
          x-large
          outlined
          depressed
          height="70"
          class="download-btn text-left"
          data-test="download-affidavit-btn"
          color="primary"
          @click="downloadAffidavit"
        >
          <v-icon
            x-large
            class="mr-3 ml-n2"
          >
            mdi-file-download-outline
          </v-icon>
          <div>
            <strong>Download Identity Affidavit</strong>
            <div class="file-size mb-1">
              PDF <span
                v-if="affidavitSize"
                v-once
              >({{ affidavitSize }})</span>
            </div>
          </div>
        </v-btn>
        <v-alert
          v-if="isDownloadFailed"
          dense
          text
          type="error"
          height="42"
          class="mt-3"
        >
          {{ downloadFailedMsg }}
        </v-alert>
      </div>
    </v-card>
    <v-divider class="my-9" />
    <div class="d-flex">
      <v-btn
        large
        color="grey lighten-2"
        class="font-weight-bold"
        data-test="back-btn"
        @click="goBack"
      >
        <v-icon class="mr-2">
          mdi-arrow-left
        </v-icon>
        Back
      </v-btn>
      <v-spacer />
      <template v-if="isAuthenticated">
        <v-btn
          large
          color="primary"
          class="font-weight-bold mr-2"
          data-test="use-existing-bceid-btn"
          @click="continueNext"
        >
          Continue
          <v-icon class="ml-2">
            mdi-arrow-right
          </v-icon>
        </v-btn>
      </template>
      <template v-else>
        <v-btn
          large
          color="primary"
          class="font-weight-bold mr-2"
          data-test="use-existing-bceid-btn"
          @click="signinUsingBCeID"
        >
          Login using existing BCeID
        </v-btn>
        <v-btn
          large
          color="primary"
          class="font-weight-bold"
          data-test="register-bceid-btn"
          @click="redirectToBceId"
        >
          Register a new BCeID
        </v-btn>
      </template>
    </div>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { IdpHint, Pages, SessionStorageKeys } from '@/util/constants'
import CommonUtils from '@/util/common-util'
import ConfigHelper from '@/util/config-helper'
import DocumentService from '@/services/document.services'
import { mapState } from 'pinia'
import { useAuthStore } from 'sbc-common-components/src/stores'

@Component({
  computed: {
    ...mapState(useAuthStore, [
      'isAuthenticated'
    ])
  }
})
export default class AffidavitDownload extends Vue {
  private downloadFailedMsg = 'Failed download'
  private isDownloadFailed = false
  private affidavitSize = ConfigHelper.getAffidavitSize() || ''

  private async downloadAffidavit () {
    try {
      this.isDownloadFailed = false
      const downloadData = await DocumentService.getAffidavitPdf()
      CommonUtils.fileDownload(downloadData?.data, `affidavit.pdf`, downloadData?.headers['content-type'])
    } catch (err) {
      // eslint-disable-next-line no-console
      console.error(err)
      this.isDownloadFailed = true
    }
  }

  private redirectToBceId () {
    window.location.href = ConfigHelper.getBceIdOsdLink()
  }

  private signinUsingBCeID () {
    this.$router.push(`/${Pages.SIGNIN}/${IdpHint.BCEID}`)
  }

  private continueNext () {
    const invToken = ConfigHelper.getFromSession(SessionStorageKeys.InvitationToken)
    const affidavitNeeded = ConfigHelper.getFromSession(SessionStorageKeys.AffidavitNeeded)
    // if affidavit flow we need to redirect user to siginin page
    //  so it will go thorough invitstion flow necessary settings like setting session and removing invitation key
    if (invToken && affidavitNeeded === 'true') {
      this.$router.push(`/${Pages.SIGNIN}/${IdpHint.BCEID}`)
    } else {
      this.$router.push(`/${Pages.CREATE_NON_BCSC_ACCOUNT}`)
    }
  }

  private goBack () {
    this.$router.push(`/${Pages.SETUP_ACCOUNT_NON_BCSC}/${Pages.SETUP_ACCOUNT_NON_BCSC_INSTRUCTIONS}`)
    window.scrollTo(0, 0)
  }
}
</script>

<style lang="scss" scoped>
  .view-container {
    max-width: 60rem;
  }

  .download-btn {
    background: #ffffff;
  }

  .file-size {
    font-size: 0.875rem;
  }

  li {
    padding-left: 0.5rem;
  }

  @media (min-width: 600px) {
    .lb {
      display: block;
    }
  }
</style>
