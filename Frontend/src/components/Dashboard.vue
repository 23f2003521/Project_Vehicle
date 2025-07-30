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
  mounted(){
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
        console.log(res)
        this.role = res.data.role;
        this.userdata = res.data;
        
        console.log(this.role)
      

      })
      .catch(err => {this.error = err.response.data.message; console.log(err);});
    },

    async exportCSV() {
  const user_id = this.userdata.user_id;

  try {
    const startTask = await axios.get(`http://127.0.0.1:5000/export_csv/${user_id}`);
    const taskId = startTask.data.task_id;

    const checkStatus = async () => {
      const res = await axios.get(`http://127.0.0.1:5000/task_status/${taskId}`, {
        validateStatus: () => true  // allow handling of non-200 responses
      });

      if (res.status === 200) {
        // Task finished, download triggered
        const blob = new Blob([res.data], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `user_${user_id}_report.csv`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } else if (res.status === 202) {
        // Still processing — try again
        alert("Preparing your file.");
        setTimeout(checkStatus, 10000);
      } else {
        alert("Task failed or invalid response.");
      }
    };

    checkStatus();
  } catch (err) {
    console.error("Error exporting CSV:", err);
    alert("Failed to start CSV export.");
  }
}


  }
};
</script>




<template>
  <div v-if="token">
    <div v-if="this.role === 'user'">


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
            <RouterLink to="/user/lot_search" class="btn-export">Lots</RouterLink>
          </div>
          <div class="search--box">
            <button @click="exportCSV" class="btn-export">Export data</button>
          </div>
 

          <router-link class="btn-export" :to="`/user/profile/${this.userdata.user_id}`">
           <i class="fas fa-user-circle fs-4"></i>
          </router-link>
        </div>
      </div>

      <!-- Parking History Table -->
      <div class="tabular-wrapper">
        <h3 class="main-title">Recent Parking History</h3>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th class="tcenter">ID</th>
                <th class="tcenter">Location</th>
                <th class="tcenter">Vehicle No</th>
                <th class="tcenter">Parking Time</th>
                <th class="tcenter">Leaving Time</th>
                <th class="tcenter">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="entry in userdata.booked_reservations" :key="entry.id">
                <td class="tcenter">{{ entry.id }}</td>
                <td class="tcenter">{{ entry.location }}</td>
                <td class="tcenter">{{ entry.vehicle_no }}</td>
                <td class="tcenter">{{ entry.parking_time }}</td>
                <td class="tcenter">{{ entry.leaving_time }}</td>
                <td class="tcenter">
                    <RouterLink v-if="entry.reservation_status === 'Booked'" :to="`/user/update_booking/${entry.id}`" class="btn btn-outline-primary fw-bold rounded px-4 py-2 flex-fill text-center">Update Booking
                    </RouterLink>
                    <RouterLink v-if="entry.reservation_status === 'Occupied'" :to="`/user/release_booking/${entry.id}`" class="btn btn-outline-danger fw-bold rounded px-4 py-2 flex-fill text-center">Release Booking
                    </RouterLink>
                  <span v-if="entry.reservation_status === 'Released'" class="btn btn-success">Parked Out</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div style="display: flex; justify-content: center; margin-top: 20px;" >
            <RouterLink to="/user/lot_search" class="btn-export">Book Reservation</RouterLink>
      </div>
      
    </div>





    </div>





<!-- Admin Dashboard  -->





     <div v-else-if="this.role === 'admin'">
    <div class="main--content">
      <!-- Header -->
      <div class="header--wrapper">
        <div class="header--title">
          <span>Welcome {{ userdata.username }}</span>
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
            
            <RouterLink :to="`/admin/update_lot/${lot.id}`" class="text-warning me-2"><i class="fas fa-pencil-alt"></i></RouterLink>
            <RouterLink :to="`/admin/delete_lot/${lot.id}`" class="text-danger"><i class="fas fa-trash-alt"></i></RouterLink>
            
            <!-- Slot Grid -->
            <div class="slot-grid mt-2">
              <div class="slot-grid">
                  <router-link v-for="(slot, i) in lot.spots" :key="i" :to="`/admin/view_spot/${slot.id}`" class="slot-box"
                    :class="{
                              available: slot.status === 'A',
                              occupied: slot.status === 'O',
                              booked: slot.status === 'B'
                            }">{{ slot.status }}</router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- Add Lot Button -->
        <div class="mt-4" style="display: flex; justify-content: center; margin-top: 20px;">
          <RouterLink to="/admin/create_lot" class="btn-export">
            <i class="fas fa-plus"></i> Add Lot
           </RouterLink>
         
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
