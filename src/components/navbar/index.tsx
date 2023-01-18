import React, { useState, useEffect } from 'react';
import {BsSun, BsMoon} from 'react-icons/bs';



const Navbar = () => {

  const [mode, setMode] = useState('night');

  const toggleMode = () => {
    setMode(mode === 'night' ? 'white' : 'night')
  }

  useEffect(() => {
    document.querySelector('html')?.setAttribute('data-theme', mode);
  }, [mode]);

  return (
<div className="navbar bg-base-100">
  <div className="flex-none">
    <div className="dropdown">
      <label tabIndex={0} className="btn btn-square btn-ghost" title='hamburguer-menu'>
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" className="inline-block w-5 h-5 stroke-current"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
      </label>
      <ul tabIndex={0} className="dropdown-content menu p-2 bg-dropdown rounded-box w-52">
        <li className='active'><a href='/'>Inicio</a></li>
        <li><a href='/'>Sobre</a></li>
      </ul>
    </div>
  </div>
  <div className="flex-1">
    <button className="btn btn-ghost normal-case text-3xl fortnite-font font-extralight text-primary">Sydney Bot</button>
  </div>
  <div className="flex-none">
    <button className="btn btn-circle btn-ghost w-16 h-16" title='mode-menu' onClick={toggleMode}>
      {mode === 'night' ? <BsSun size={20} /> : <BsMoon size={20} />}
    </button>
  </div>
</div>
  )
}

export default Navbar