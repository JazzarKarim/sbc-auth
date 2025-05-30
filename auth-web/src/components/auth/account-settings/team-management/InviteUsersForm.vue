<template>
  <div>
    <p data-test="inviteUserFormText">
      {{ inviteUserFormText }}
    </p>
    <v-form
      ref="form"
      class="mt-9"
    >
      <div class="invite-list">
        <transition-group name="slide-y-transition">
          <div
            v-for="(invite, index) in invitations"
            :key="index + 1"
            class="d-flex"
          >
            <v-text-field
              v-model="invitations[index].emailAddress"
              dense
              filled
              label="Email Address"
              :rules="emailRules"
              :data-test="getIndexedTag('email-address', index)"
            />

            <v-overflow-btn
              v-model="invitations[index].selectedRole.name"
              filled
              hide-details
              class="select-role-btn ml-2"
              item-text="name"
              item-value="name"
              menu-props="dense"
              :items="availableRoles"
              :value="availableRoles[0]"
              :data-test="getIndexedTag('role-selector', index)"
            >
              <template #selection="{ item }">
                {{ item.displayName }}
              </template>

              <template #item="{ item }">
                <div class="role-menu-item">
                  <v-list-item-icon>
                    <v-icon v-text="item.icon" />
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>{{ item.displayName }}</v-list-item-title>
                    <v-list-item-subtitle>{{ item.label }}</v-list-item-subtitle>
                  </v-list-item-content>
                </div>
              </template>
            </v-overflow-btn>

            <v-btn
              icon
              class="mt-3 ml-1"
              @click="removeEmail(index)"
            >
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </div>
        </transition-group>
      </div>
      <v-btn
        text
        small
        color="primary"
        class="pr-3 pl-1"
        data-test="add-another-button"
        @click="addEmail()"
      >
        <v-icon>mdi-plus-box</v-icon>
        <span>Add Another</span>
      </v-btn>
      <div class="form__btns">
        <v-btn
          large
          depressed
          color="primary"
          :loading="loading"
          :disabled="loading || !isFormValid()"
          data-test="send-invites-button"
          @click="sendInvites"
        >
          <span>Send Invites</span>
        </v-btn>
        <v-btn
          large
          depressed
          class="ml-2"
          data-test="cancel-button"
          @click="cancel"
        >
          <span>Cancel</span>
        </v-btn>
      </div>
    </v-form>
  </div>
</template>

<script lang="ts">
import { Action, State } from 'pinia-class'
import { Component, Emit } from 'vue-property-decorator'
import { MembershipType, RoleInfo } from '@/models/Organization'
import CommonUtils from '@/util/common-util'
import { Invitation } from '@/models/Invitation'
import { Role } from '@/util/constants'
import TeamManagementMixin from '../../mixins/TeamManagementMixin.vue'
import { useOrgStore } from '@/stores/org'
import { useUserStore } from '@/stores/user'

interface InvitationInfo {
  emailAddress: string
  role: RoleInfo
  selectedRole?: RoleInfo
}

@Component({})
export default class InviteUsersForm extends TeamManagementMixin {
  private loading = false
  @State(useOrgStore) private readonly pendingOrgInvitations!: Invitation[]
  @Action(useOrgStore) private readonly resetInvitations!: () => void
  @Action(useOrgStore) private readonly createInvitation!: (Invitation) => Promise<void>
  @Action(useOrgStore) private readonly resendInvitation!: (Invitation) => Promise<void>
  @State(useUserStore) private roleInfos!: RoleInfo[]

  $refs: {
    form: HTMLFormElement
  }

  private get availableRoles () {
    const isStaffManageAccounts = this.currentUser?.roles?.includes(Role.StaffManageAccounts)
    if ((this.currentMembership.membershipTypeCode !== MembershipType.Admin) && !isStaffManageAccounts) {
      return this.roles.filter(role => role.name !== MembershipType.Admin)
    }
    return this.roles
  }

  private invitations: InvitationInfo[] = []
  private emailRules = CommonUtils.emailRules(true)

  private roles: RoleInfo[] = []

  private getIndexedTag (tag, index): string {
    return `${tag}-${index}`
  }

  private created () {
    this.roles = this.roleInfos
    for (let i = 0; i < 3; i++) {
      this.invitations.push({ emailAddress: '', role: this.roles[0], selectedRole: { ...this.roles[0] } })
    }
  }

  private hasDuplicates (): boolean {
    const invitations = this.invitations.filter(invitation => invitation.emailAddress)
    return new Set(invitations.map(invitation => invitation.emailAddress.toLowerCase())).size !== invitations.length
  }

  private isFormValid (): boolean {
    return this.invitations &&
            this.invitations.some(invite => invite.emailAddress) &&
            !this.hasDuplicates() &&
            this.$refs.form.validate()
  }
  private removeEmail (index: number) {
    this.invitations.splice(index, 1)
  }

  private addEmail () {
    this.invitations.push({ emailAddress: '', role: this.roles[0], selectedRole: { ...this.roles[0] } })
  }

  private resetForm () {
    this.invitations.forEach(invitation => {
      invitation.emailAddress = ''
      invitation.role = this.roles[0]
      invitation.selectedRole = { ...this.roles[0] }
    })
  }

  private async sendInvites () {
    if (this.isFormValid()) {
      // set loading state
      this.loading = true
      this.resetInvitations()
      for (let i = 0; i < this.invitations.length; i++) {
        const invite = this.invitations[i]
        if (invite && invite.emailAddress) {
          // Check if there is a pending invitation for this address already
          const existingInvitation = this.pendingOrgInvitations.find(pendingInvitation =>
            pendingInvitation.recipientEmail.toLowerCase() === invite.emailAddress.toLowerCase())

          if (existingInvitation) {
            await this.resendInvitation(existingInvitation)
          } else {
            await this.createInvitation({
              recipientEmail: invite.emailAddress,
              sentDate: new Date(),
              membership: [{ membershipType: invite.selectedRole.name.toUpperCase(), orgId: this.currentOrganization.id }]
            })
          }
        }
      }

      this.resetForm()

      // emit event to let parent know the invite sequence is complete
      this.$emit('invites-complete')
      this.loading = false
    }
  }

  @Emit()
  private cancel () {
    this.resetForm()
  }
}
</script>

<style lang="scss" scoped>
  .invite-list {
    margin: 0;
    padding: 0;
  }

  .invite-list .select-role {
    width: 8rem;
  }

  .form__btns {
    display: flex;
    flex-direction: row;
    justify-content: flex-end;
  }

  .role-menu-item {
    display: flex;
    width: 24rem;

    .v-list-item__title {
      margin-bottom: 0.25rem;
      font-size: 0.875rem;
      font-weight: 700;
    }

    .v-list-item__subtitle {
      white-space: normal;
      overflow: visible;
      line-height: 1rem;
      font-size: 0.812rem;
    }
  }

  .v-list-item.active {
    background: $BCgovBlue0;
  }

  .select-role-btn {
    width: 9rem;

    ::v-deep .v-input__slot {
      padding-right: 0 !important
    }
  }
</style>
