<template>
 <div>
  <v-row>
    <v-col
      xs="12"
      sm="6"
      class="d-flex"
      v-for="authOption in authOptions"
      :key="authOption.type"
    >
      <v-card
        flat
        outlined
        hover
        class="account-card elevation-2 pa-8 d-flex flex-column text-center"
        :class="{ 'active': authType === authOption.type }"
        @click="selectAuthType(authOption.type)"
      >
        <div class="account-type__icon mb-8">
          <v-icon color="grey">{{authOption.icon}}</v-icon>
        </div>
        <div class="account-type__title font-weight-bold mb-6">
          {{authOption.title}}
        </div>
        <div class="account-type__details mb-10">
          {{authOption.description}}
        </div>
        <div class="account-type__buttons">
          <v-btn
            v-if="showLearnMore"
            large
            depressed
            block
            color="primary"
            class="font-weight-bold mb-3"
            outlined
            @click="selectLearnMore(authOption.type)"
          >
            LEARN MORE
          </v-btn>
          <v-btn
            large
            depressed
            block
            color="primary"
            class="font-weight-bold"
            :outlined="authType != authOption.type"
            @click="selectAuthType(authOption.type)"
          >
            {{ authType == authOption.type ? 'SELECTED' : 'SELECT' }}
          </v-btn>
        </div>
       </v-card>
      </v-col>
    </v-row>
    <LearnMoreBCSC ref="bcscLearnMoreDialog" @bcsc-selected="selectAuthType('BCSC')" />
    <LearnMoreBCEID ref="bceidLearnMoreDialog" @bceid-selected="selectAuthType('BCEID')" />
  </div>
</template>

<script lang="ts">
import { Component, Emit, Mixins } from 'vue-property-decorator'
import { LDFlags, LoginSource } from '@/util/constants'
import { mapActions, mapMutations, mapState } from 'vuex'
import AccountChangeMixin from '@/components/auth/mixins/AccountChangeMixin.vue'
import AccountMixin from '@/components/auth/mixins/AccountMixin.vue'
import LaunchDarklyService from 'sbc-common-components/src/services/launchdarkly.services'
import LearnMoreBCEID from '@/components/auth/common/LearnMoreBCEID.vue'
import LearnMoreBCSC from '@/components/auth/common/LearnMoreBCSC.vue'
import { Organization } from '@/models/Organization'

@Component({
  components: {
    LearnMoreBCEID,
    LearnMoreBCSC
  },
  computed: {
    ...mapState('org', [
      'currentOrganization',
      'memberLoginOption'
    ])
  },
  methods: {
    ...mapActions('org', [
      'syncMemberLoginOption',
      'updateLoginOption'
    ]),
    ...mapMutations('org', ['setMemberLoginOption'])
  }
})
export default class AccountLoginOptionPicker extends Mixins(AccountChangeMixin, AccountMixin) {
  private btnLabel = 'Save'
  private readonly memberLoginOption!: LoginSource
  private readonly syncMemberLoginOption!: (currentAccount: number) => string
  protected readonly syncOrganization!: (
    currentAccount: number
  ) => Promise<Organization>
  private readonly updateLoginOption!: (loginType: string) => Promise<string>

  private errorMessage: string = ''

  private authType = LoginSource.BCSC

  private authOptions = [
    {
      type: LoginSource.BCSC,
      title: 'BC Services Card',
      description: `Use your BC Services Card with a mobile app or 
                    a USB card reader to verify your identity.`,
      icon: 'mdi-account-card-details-outline'
    },
    {
      type: LoginSource.BCEID,
      title: 'BCeID and 2-factor authentication app',
      description: `Login with a BCeID combined with a verification code in a mobile app, 
                    such as Google or Microsoft Authenticator.`,
      icon: 'mdi-two-factor-authentication'
    }
  ]

  $refs: {
    bcscLearnMoreDialog: LearnMoreBCSC,
    bceidLearnMoreDialog: LearnMoreBCEID
  }

  @Emit('auth-type-selected')
  private selectAuthType (authType: LoginSource) {
    this.authType = authType
    return authType
  }

  private selectLearnMore (authType: LoginSource) {
    switch (authType) {
      case LoginSource.BCSC:
        // open up BCSC learn more dialog
        window.open('https://www2.gov.bc.ca/gov/content/governments/government-id/bc-services-card/log-in-with-card', '_blank')
        break
      case LoginSource.BCEID:
        // open up BCEID learn more dialog
        this.$refs.bceidLearnMoreDialog.open()
        break
      default:
        // do nothing
    }
  }

  private get showLearnMore (): boolean {
    return LaunchDarklyService.getFlag(LDFlags.AuthLearnMore) || false
  }

  private get loginSourceEnum () {
    return LoginSource
  }

  private async mounted () {
    if (!this.memberLoginOption) {
      await this.syncMemberLoginOption(this.getAccountFromSession().id)
    }
    this.authType = this.memberLoginOption ? this.memberLoginOption : this.authType
  }
}
</script>

<style lang="scss" scoped>
  @import '$assets/scss/theme.scss';

  .account-card {
    display: flex;
    flex-direction: column;
    position: relative;
    width: 100%;
    background-color: #ffffff !important;
    transition: all ease-out 0.2s;

    &:hover {
      border-color: var(--v-primary-base) !important;

      .v-icon {
        color: var(--v-primary-base) !important;
      }
    }

    &.active {
      box-shadow: 0 0 0 2px inset var(--v-primary-base), 0 3px 1px -2px rgba(0,0,0,.2),0 2px 2px 0 rgba(0,0,0,.14),0 1px 5px 0 rgba(0,0,0,.12) !important;
    }
  }

  .theme--light.v-card.v-card--outlined.active {
    border-color: var(--v-primary-base);
  }

  .account-card .v-icon {
    color: var(--v-grey-lighten1) !important;
    font-size: 3rem !important;
  }

  .account-card.active .v-icon {
    color: var(--v-primary-base) !important;
  }

  .account-type {
    flex: 1 1 auto;
  }

  .account-type__icon {
    flex: 0 0 auto;
  }

  .account-type__title {
    flex: 0 0 auto;
    line-height: 1.75rem;
    font-size: 1.5rem;
    font-weight: 700;
  }

  .account-type__details {
    flex: 1 1 auto;
  }
</style>