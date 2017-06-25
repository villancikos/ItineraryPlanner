import React, {Component} from 'react'
import {render} from 'react-dom';
import { AppContainer } from 'react-hot-loader';
import Greeter from './Greeter';

// import '../sass/project.scss';

render(
  <AppContainer>
    <Greeter/>
  </AppContainer>,
  document.getElementById('root')
);
      

if (module.hot) {
  module.hot.accept('./Greeter', function() {
    console.log('Accepting the updated library module!');
  })
}