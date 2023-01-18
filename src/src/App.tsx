import {
  BrowserRouter as Router,
  Routes,
  Route,
} from 'react-router-dom';

import HOME from "./pages/home";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HOME/>}/>
      </Routes>
    </Router>
  );
}

export default App;
