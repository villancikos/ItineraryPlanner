import React, {Component} from 'react'
import {render} from 'react-dom';

// import '../sass/project.scss';

class Greeter extends Component{
  render() {
    return (
      <div>
        Test
      </div>
    );
  }
}

render(<Greeter />, document.getElementById('root'));
      
