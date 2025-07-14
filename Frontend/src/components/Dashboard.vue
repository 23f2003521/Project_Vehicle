<script>
import axios from 'axios';

export default {
  data() {
    return {
      token: "",
      role: "",
      userdata: "",
      error: ""
    };
  },
  mounted() {
    this.loadtoken();
    this.loaduser();
  },
  methods: {
    loadtoken() {
      const token = localStorage.getItem('token');
      if (token) {
        this.token = token;
      }
    },
    loaduser: function() {
        const response=axios.get("http://127.0.0.1:5000/api/dashboard",
       {
        headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Authorization": `Bearer ${this.token}`
        }
      }) 
      response
      .then(res => {
        this.role = res.data.role;
        this.userdata = res.data;
        console.log(res)

      })
      .catch(err => {this.error = err.response.data.message; console.log(this.error);});
    }
  }
};
</script>




<template>
  <div v-if="token">
    <div v-if="role === 'user'">


    <!-- Main Content -->
    <div class="main--content">
      <!-- Header -->
      <div class="header--wrapper">
        <div class="header--title">
          <span>Welcome {{ userdata.username }}</span>
          <h2>Dashboard</h2>
        </div>
        <div class="user--info">
          <div class="search--box">
            <!-- <form :action="`/user_find/${user_id}`" method="post">
              <select name="criteria">
                <option value="">Select Category</option>
                <option value="education">Education</option>
                <option value="medical">Medical</option>
                <option value="infrastructure">Infrastructure</option>
                <option value="agriculture">Agriculture</option>
              </select>
              <input type="search" name="search" placeholder="Search">
              <button class="btn btn-success">Search</button>
            </form> -->
          </div>
          <!-- <a :href="`/profile/${user_id}`">
            <img :src="`/static/uploads/profile_images/${user_id}.jpeg`" alt="Profile" width="40">
          </a> -->
        </div>
      </div>

      <!-- Parking History Table -->
      <div class="tabular-wrapper">
        <h3 class="main-title">Recent Parking History</h3>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Location</th>
                <th>Vehicle No</th>
                <th>Timestamp</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="entry in userdata.booked_reservations" :key="entry.id">
                <td>{{ entry.id }}</td>
                <td>{{ entry.location }}</td>
                <td>{{ entry.vehicle_no }}</td>
                <td>{{ entry.timestamp }}</td>
                <td>
                 <button
                    v-if="entry.reservation_status === 'Booked'"
                    class="btn btn-danger">Release</button>
                  <span
                    v-else
                    class="btn btn-success">Parked Out</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>





    </div>

<!-- Admin Dashboard  -->
     <div v-else-if="role === 'admin'">
    <div class="main--content">
      <!-- Header -->
      <div class="header--wrapper">
        <div class="header--title">
          <span>Welcome {{ userdata.username }}</span>
          <h2>Dashboard</h2>
        </div>
        <div class="user--info">
          <div class="search--box"></div>
        </div>
      </div>

      <!-- Parking Lots Section -->
      <div class="card-container">
        <h3 class="main-title">Parking Lots</h3>
        <div class="d-flex flex-wrap">
          <div
            v-for="(lot, index) in userdata.lots"
            :key="lot.id"
            class="lot-card m-3 p-3 border rounded shadow-sm"
            style="width: 260px;"
          >
            <h5 class="fw-bold">{{ lot.prime_address }}</h5>
            
            <RouterLink to="#" class="text-warning me-2"><i class="fas fa-pencil-alt"></i></RouterLink>
            <RouterLink to="#" class="text-danger"><i class="fas fa-trash-alt"></i></RouterLink>
            
            <!-- Slot Grid -->
            <div class="slot-grid mt-2">
              <div
                v-for="(slot, i) in lot.spots"
                :key="i"
                class="slot-box"
                :class="{
                            'available': slot.status === 'A',
                            'occupied': slot.status === 'O',
                            'booked': slot.status === 'B'
}"
              >
                {{ slot.status }}
              </div>
            </div>
          </div>
        </div>

        <!-- Add Lot Button -->
        <div class="mt-4">
          <button class="btn btn-warning fw-bold rounded px-4 py-2">+ Add Lot</button>
        </div>
      </div>
    </div>
  </div>

  </div>
  <div v-else class="text-center">
    Please login
  </div>
</template>



<style scoped>
/* Slot grid styling */
.slot-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 6px;
  margin-top: 10px;
}

.slot-box {
  width: 30px;
  height: 30px;
  font-weight: bold;
  font-size: 14px;
  text-align: center;
  line-height: 30px;
  border-radius: 6px;
  box-shadow: 0 0 4px rgba(0, 0, 0, 0.1);
}

.available {
  background-color: lightgreen;
  color: black;
}

.occupied {
  background-color: lightcoral;
  color: white;
}
.booked {
  background-color: rgb(244, 244, 116);
  color: black;
}
</style>
