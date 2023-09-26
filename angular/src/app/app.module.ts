import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule} from "@angular/forms"
import { Router, RouterModule, Routes } from '@angular/router';

import { AppComponent } from './app.component';
import { SkillsComponent } from './components/skills/skills.component';
import { SkillItemComponent } from './components/skill-item/skill-item.component';
import { AddSkillComponent } from './components/add-skill/add-skill.component';

const appRoutes: Routes = [
  {path: "skills", component: SkillsComponent},
]

@NgModule({
  declarations: [
    AppComponent,
    SkillsComponent,
    SkillItemComponent,
    AddSkillComponent,
  ],
  imports: [
    BrowserModule,
    FontAwesomeModule,
    HttpClientModule,
    FormsModule,
    RouterModule.forRoot(appRoutes, {enableTracing:true})
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
