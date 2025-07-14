<script>
export default {
  methods: {
    toLogin: function() {
      this.$router.push("/login")
    }
  }
}
</script>


<template>
  <div>
    <!-- Hero Section -->
    <section class="hero">
      <img
  class="hero-image"
  src="../assets/bg.jpg"
  alt="A parking area where some parked vehicles and some are coming to be parked"
  onerror="this.style.display='none'"
/>

      <div class="hero-content">
        <h1>Welcome to <span style="color: #49b675;">SmartPark</span> – Your Hassle-Free Parking Solution</h1>
        <p>
          Say goodbye to parking woes! With SmartPark, find and book parking spots in seconds. Enjoy real-time availability, cashless payments, and smart reminders.</p>
        <button @click="toLogin"  class="btn-orange big">Get Started</button>
        
      </div>
    </section>

    <!-- Features Section -->
    <section class="features">
      <div class="feature">
        <h3>Real-Time Availability</h3>
        <p>See which spots are open and book instantly. No more circling around in frustration.</p>
      </div>
      <div class="feature">
        <h3>Cashless & Secure Payments</h3>
        <p>Integrated digital payments let you park stress-free with just a few taps.</p>
      </div>
      <div class="feature">
        <h3>Smart Reminders</h3>
        <p>Get notified before your time ends and extend your stay remotely, anytime.</p>
      </div>
    </section>
  </div>
</template>


<style scoped>
/* Reset & base */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  background: #fff;
  color: #111;
}

.btn-orange {
  background-color: #712898;
  border: none;
  color: white;
  padding: 0.65rem 1.5rem;
  font-weight: 700;
  font-size: 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-orange:hover {
  background-color: #c032b6;
}

/* Hero Section */
.hero {
  position: relative;
  text-align: center;
  color: white;
  overflow: hidden;
}

.hero-image {
  width: 100%;
  max-height: 400px;
  object-fit: cover;
  filter: brightness(0.6);
  user-select: none;
}

.hero-content {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  max-width: 900px;
  padding: 1rem 2rem;
  transform: translate(-50%, -50%);
  background-color: rgba(0, 0, 0, 0.4);
  border-radius: 12px;
}

.hero-content h1 {
  font-size: 2.2rem;
  font-weight: 900;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.8);
}

.hero-content p {
  font-weight: 400;
  font-size: 1.25rem;
  margin-bottom: 1rem;
  text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.6);
}

.hero-content ul {
  list-style: none;
  padding-left: 0;
  margin-bottom: 1.5rem;
}

.hero-content ul li {
  font-size: 1rem;
  margin: 0.5rem 0;
  text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.6);
}

.hero-content .big {
  font-size: 1.25rem;
  padding: 0.85rem 2.5rem;
}

.email-input {
  margin-top: 1rem;
  width: 100%;
  max-width: 320px;
  font-size: 1rem;
  padding: 0.7rem 1rem;
  border-radius: 4px;
  border: none;
  outline: none;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.15);
  transition: box-shadow 0.3s ease;
}

.email-input:focus {
  box-shadow: 0 0 8px #49b675;
}

/* Features Section */
.features {
  display: flex;
  max-width: 900px;
  margin: 4rem auto 6rem auto;
  gap: 3rem;
  padding: 0 1rem;
  justify-content: center;
  flex-wrap: wrap;
  color: #333;
  text-align: center;
}

.feature {
  flex: 1 1 280px;
  padding: 1.5rem 1.2rem;
  border-radius: 8px;
  background-color: #f5f5f5;
}

.feature h3 {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #49b675;
}

.feature p {
  font-weight: 400;
  font-size: 1rem;
  line-height: 1.4;
  color: #555;
}

/* Responsive */
@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 1.7rem;
  }
  
  .hero-content p {
    font-size: 1rem;
  }

  .features {
    flex-direction: column;
    max-width: 100%;
    margin: 3rem auto;
  }
}
</style>
