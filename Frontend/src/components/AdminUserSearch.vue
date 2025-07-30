
<script>
import axios from 'axios';

export default {
  data() {
    return {
      users: [],
      message: ''
    };
  },
  mounted() {
    this.fetchUsers();
  },
  methods: {
    fetchUsers() {
      axios.get('http://127.0.0.1:5000/api/admin/user_search', {
        headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Authorization": `Bearer ${localStorage.getItem('token')}`
        }
      })
      .then(res => {
        this.users=res.data;
        this.message=res.data.message
        
      })
      .catch(err => {
        this.message = "Error fetching user data";
        console.log(err);
      });
    }
  }
}
</script>


<template>
  <div class="main--content">
       <!-- Header -->
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


          <router-link to="/user/profile/1" class="btn-export">
           <i class="fas fa-user-circle fs-4"></i>
          </router-link>
        </div>
      </div>
      <div class="tabular-wrapper">
        <h3 class="main-title">All Registered Users</h3>
        <div class="table-container" v-if="users.length > 0">
          <table>
            <thead>
              <tr>
                <th class="tcenter">ID</th>
                <th class="tcenter">User Name</th>
                <th class="tcenter">Email</th>
                <th class="tcenter">Vehicle Number</th>
                <th class="tcenter">Total Reservations</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id">
                <td class="tcenter">{{ user.id }}</td>
                <td class="tcenter">{{ user.name }}</td>
                <td class="tcenter">{{ user.email }}</td>
                <td class="tcenter">{{ user.vehicle_no}}</td>
                <td class="tcenter">{{ user.no_of_reservations}}</td>
              </tr>
        </tbody>
      </table>
     </div>
     <div v-else>
      <p class="text-danger">{{ message }}</p>
    </div>
    </div>

 </div>

</template>









<style>

</style>