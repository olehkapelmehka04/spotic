import {BrowserRouter, Routes, Route} from 'react-router-dom';

import Main from "./page/Main";
import Validation from "./page/Validation";
import MainSongPage from "./page/MainSongPage";
import PlayLists from "./page/PlayLists";
import WaveUser from "./page/WaveUser";
import ProfilerUser from "./page/ProfilerUser";

function App() {
  return (
    <BrowserRouter>
        <Routes>
            <Route path="/" element={<Main/>} />

            <Route path="/validation" element={<Validation/>} />

            <Route path="/main" element={<MainSongPage/>} />
            <Route path="/PlayList" element={<PlayLists/>} />
            <Route path="/MyWave" element={<WaveUser/>} />
            <Route path="/Profile" element={<ProfilerUser/>} />
        </Routes>
    </BrowserRouter>
    )
}

export default App
