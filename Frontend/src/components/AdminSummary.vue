<script>
import SummaryChart from "./SummaryChart.vue"

export default {
  components: {
    SummaryChart
  }
}
</script>





<template>
  <div class="main-content">
       <div class="header--wrapper">
        <div class="header--title">
          <span>Welcome Admin</span>
          <h2>Dashboard</h2>
        </div>
        <div class="user--info">
          <div class="search--box">
            <RouterLink to="/admin/user_search" class="btn-export">Users</RouterLink>
          </div>
          <div class="search--box">
            <RouterLink to="/admin/lot_search" class="btn-export">Lots</RouterLink>
          </div>


          <router-link :to="`/user/profile/1`" class="btn-export">
           <i class="fas fa-user-circle fs-4"></i>
          </router-link>
        </div>
      </div>
      
  <div class="p-6">
    <div class="row">
      <SummaryChart endpoint="http://localhost:5000/api/reservations_per_day" />
      <SummaryChart endpoint="http://localhost:5000/api/revenue_per_day" />
      <SummaryChart endpoint="http://localhost:5000/api/lots_by_location" />
      <SummaryChart endpoint="http://localhost:5000/api/most_occupied_lots" />
      <SummaryChart endpoint="http://localhost:5000/api/most_booked_lots" />
      <SummaryChart endpoint="http://localhost:5000/api/least_used_lots" />
      <SummaryChart endpoint="http://localhost:5000/api/lots_by_price_range" />
    </div>
  </div>
  </div>
  
</template>