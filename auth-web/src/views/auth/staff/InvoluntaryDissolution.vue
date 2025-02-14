<template>
  <v-container
    id="involuntary-dissolution"
    class="view-container"
  >
    <!-- Spinner while waiting to grab the number of the businesses ready for D1 Dissolution -->
    <v-fade-transition>
      <div
        v-if="isLoading"
        class="loading-container"
      >
        <v-progress-circular
          size="50"
          width="5"
          color="primary"
          :indeterminate="isLoading"
        />
      </div>
    </v-fade-transition>
    <div class="view-header flex-column">
      <h1>
        Staff Involuntary Dissolution Batch
      </h1>
      <p class="mt-2 mb-0">
        B.C. Business Ready for D1 Dissolution: {{ businessesReadyforDissolutionNumber }}
      </p>
    </div>

    <!-- Automated Dissolution Section -->
    <section>
      <v-row>
        <v-col
          cols="12"
          lg="9"
        >
          <header>
            <h2>Automated Dissolution</h2>
            <p class="mt-2">
              You can set up a schedule to automate the involuntary dissolution process.
              The system will prioritize the oldest eligible businesses to move into D1 dissolution,
              automatically saving a list of businesses in each batch to the LAN.
              The schedule will run until there are no more businesses ready for D1 dissolution.
              To pause the schedule, enter a batch size of 0.
            </p>
          </header>
        </v-col>
      </v-row>
      <v-row>
        <v-col
          cols="12"
          lg="9"
        >
          <v-card
            id="company-summary-vcard"
            flat
            class="mt-2"
          >
            <CardHeader
              badgeText="Paused"
              icon="mdi-calendar-clock"
              label="Automated Dissolution Schedule"
            />
            <DissolutionSchedule />
          </v-card>
        </v-col>
      </v-row>
    </section>
  </v-container>
</template>

<script lang="ts">
import { defineComponent, onMounted, reactive, toRefs } from '@vue/composition-api'
import { CardHeader } from '@/components'
import DissolutionSchedule from '@/components/auth/staff/DissolutionSchedule.vue'
import { useStaffStore } from '@/stores/staff'

export default defineComponent({
  name: 'InvoluntaryDissolution',
  components: {
    CardHeader,
    DissolutionSchedule
  },
  setup () {
    const state = reactive({
      businessesReadyforDissolutionNumber: -1,
      isLoading: true
    })
    const staffStore = useStaffStore()

    onMounted(async () => {
      // Make the call to get the involuntary dissolutions statistics data and set it in store
      await staffStore.getDissolutionStatistics()
      state.businessesReadyforDissolutionNumber = staffStore.dissolutionStatistics?.data?.eligibleCount

      // Hide spinner
      state.isLoading = false
    })

    return {
      ...toRefs(state)
    }
  }
})
</script>

<style lang="scss" scoped>
h2 {
  font-size: $px-18;
}

p {
  font-size: $px-16;
}

// Tighten up some of the spacing between rows
[class^="col"] {
  padding-top: 0;
}
</style>
